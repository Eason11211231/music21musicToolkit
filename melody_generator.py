from music21 import stream, note, meter, key as m21key, instrument
import dropbox
import os
import uuid
import random

DROPBOX_ACCESS_TOKEN = "sl.xxxxx.你的_token"  # TODO: 換掉你的 dropbox token
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# ✅ 中文調性轉換 + 自動大小寫處理
def key_translate(input_str):
    if not input_str:
        return "C"

    mapping = {
        "大調": "major",
        "小調": "minor",
        "升": "#",
        "降": "b"
    }

    for zh, en in mapping.items():
        input_str = input_str.replace(zh, en)

    return input_str.strip().title()

def generate_melody(style, key_str, time_signature, measures=8, pitch_pool=None):
    score = stream.Score()

    # ✅ 用 key_translate 處理中文調性與大小寫
    translated_key_str = key_translate(key_str)
    try:
        k = m21key.Key(translated_key_str)
    except Exception as e:
        print(f"[ERROR] 無法解析 key：'{key_str}'（轉為：'{translated_key_str}'）錯誤：{e}")
        return {"error": f"無法解析調性：{key_str}"}

    try:
        ts = meter.TimeSignature(time_signature)
    except:
        ts = meter.TimeSignature("4/4")

    melody = stream.Part()
    melody.id = "Melody"
    melody.partName = "旋律"
    melody.append(instrument.Violin())
    melody.append(k)
    melody.append(ts)

    bass = stream.Part()
    bass.id = "Bass"
    bass.partName = "低音"
    bass.append(instrument.Violoncello())
    bass.append(k)
    bass.append(ts)

    # pitchPool 清理處理
    if pitch_pool and isinstance(pitch_pool, list):
        cleaned_pitch_pool = []
        for p in pitch_pool:
            try:
                n = note.Note(p)
                cleaned_pitch_pool.append(n.nameWithOctave)
            except Exception as e:
                print(f"[Warning] 跳過不合法音符 '{p}': {e}")
        scale_pitches = cleaned_pitch_pool if cleaned_pitch_pool else [str(p.nameWithOctave) for p in k.getPitches("C3", "C6")]
    else:
        scale_pitches = [str(p.nameWithOctave) for p in k.getPitches("C3", "C6")]

    for _ in range(measures):
        m1 = stream.Measure()
        m2 = stream.Measure()
        offset = 0.0

        motif = random.choice([
            [1.0, 1.0, 1.0, 1.0],
            [0.5, 0.5, 1.0, 2.0],
            [2.0, 1.0, 1.0]
        ])

        for dur in motif:
            pitch_str = random.choice(scale_pitches)
            try:
                n1 = note.Note(pitch_str)
                n1.quarterLength = dur
                m1.insert(offset, n1)

                n2 = note.Note(pitch_str).transpose(-12)
                n2.quarterLength = dur
                m2.insert(offset, n2)

                offset += dur
            except Exception as e:
                print(f"[Warning] 音符生成錯誤：{e}")
                continue

        melody.append(m1)
        bass.append(m2)

    score.insert(0, bass)
    score.insert(0, melody)

    filename = f"melody_{uuid.uuid4().hex}.musicxml"
    score.write('musicxml', fp=filename)

    with open(filename, "rb") as f:
        dbx.files_upload(f.read(), f"/{filename}", mode=dropbox.files.WriteMode.overwrite)

    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(f"/{filename}")
    public_url = shared_link_metadata.url.replace("?dl=0", "?dl=1")

    os.remove(filename)
    return public_url  # ✅ 這一行正確縮排在函式裡面！

from music21 import stream, note, meter, key as m21key, instrument
import dropbox
import os
import uuid
import random

DROPBOX_ACCESS_TOKEN = "sl.xxxxx.你的_token"  # TODO: 請換成你自己的 Dropbox token
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def generate_melody(style, key_str, time_signature, measures=8, pitch_pool=None):
    score = stream.Score()

    # Key 處理
    try:
        cleaned_key_str = key_str.strip().title() if key_str else "C"
        k = m21key.Key(cleaned_key_str)
    except Exception as e:
        print(f"[Warning] key_str 無法解析 '{key_str}', fallback to C: {e}")
        k = m21key.Key("C")

    # Time signature 處理
    try:
        ts = meter.TimeSignature(time_signature)
    except:
        ts = meter.TimeSignature("4/4")

    # 建立旋律與低音部
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

    # 處理 pitch_pool
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
    return public_url  # ✅ 確保在函式內，縮排對齊

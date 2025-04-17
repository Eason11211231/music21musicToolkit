from music21 import stream, note, meter, key as m21key
import random
import dropbox
import os
import uuid

# 請貼上你自己的 Dropbox token 👇
DROPBOX_ACCESS_TOKEN = "sl.xxxxx.你的_token"
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def generate_melody(style, key_str, time_signature, measures=8):
    score = stream.Score()

    # 嘗試解析調性與拍號
    try:
        k = m21key.Key(key_str)
    except:
        k = m21key.Key("C")

    try:
        ts = meter.TimeSignature(time_signature)
    except:
        ts = meter.TimeSignature("4/4")

from music21 import instrument

melody = stream.Part()
melody.id = "Melody"
melody.partName = "旋律"
melody.append(instrument.Violin())  # ✅ 指定旋律為小提琴
melody.append(k)
melody.append(ts)

bass = stream.Part()
bass.id = "Bass"
bass.partName = "低音"
bass.append(instrument.Cello())  # ✅ 指定低音為大提琴
bass.append(k)
bass.append(ts)

scale_pitches = k.getPitches()

for _ in range(measures):
        m1 = stream.Measure()
        m2 = stream.Measure()

        for i in range(4):  # 每拍 1 音
            offset = i * 1.0

            # Melody
            pitch_m = random.choice(scale_pitches)
            n1 = note.Note(pitch_m)
            n1.quarterLength = 1.0
            m1.insert(offset, n1)

            # Bass
            pitch_b = random.choice(scale_pitches).transpose(-12)
            n2 = note.Note(pitch_b)
            n2.quarterLength = 1.0
            m2.insert(offset, n2)

        melody.append(m1)
        bass.append(m2)

    # 插入兩個聲部（先低音，再旋律）
    score.insert(0, bass)
    score.insert(0, melody)

    # 產生 MusicXML 檔案並上傳 Dropbox
    filename = f"melody_{uuid.uuid4().hex}.musicxml"
    score.write('musicxml', fp=filename)

    with open(filename, "rb") as f:
        dbx.files_upload(f.read(), f"/{filename}", mode=dropbox.files.WriteMode.overwrite)

    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(f"/{filename}")
    public_url = shared_link_metadata.url.replace("?dl=0", "?dl=1")

    os.remove(filename)
    return public_url

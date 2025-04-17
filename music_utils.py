from music21 import stream, note, meter, key as m21key
import random
import dropbox
import os
import uuid

# 👉 你的 Dropbox access token 放這裡
DROPBOX_ACCESS_TOKEN = "sl.xxxxx.your_token"
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def generate_melody(style, key_str, time_signature, measures=8):
    score = stream.Score()

    # 安全解析 key 與拍號
    try:
        k = m21key.Key(key_str)
    except:
        k = m21key.Key("C")

    try:
        ts = meter.TimeSignature(time_signature)
    except:
        ts = meter.TimeSignature("4/4")

    # 建立兩個獨立聲部
    melody = stream.Part()
    melody.id = "Melody"
    melody.partName = "旋律"
    melody.append(k)
    melody.append(ts)

    bass = stream.Part()
    bass.id = "Bass"
    bass.partName = "低音"
    bass.append(k)
    bass.append(ts)

    # 抓取調內音階音
    scale_pitches = k.getPitches()

    # 🎯 每個小節：同時建立旋律與低音，並在每拍插入 offset
    for _ in range(measures):
        m1 = stream.Measure()
        m2 = stream.Measure()

        for i in range(4):  # 每拍
            offset = i * 1.0

            # Melody Note
            pitch_m = random.choice(scale_pitches)
            n1 = note.Note(pitch_m)
            n1.quarterLength = 1.0
            m1.insert(offset, n1)

            # Bass Note
            pitch_b = random.choice(scale_pitches).transpose(-12)
            n2 = note.Note(pitch_b)
            n2.quarterLength = 1.0
            m2.insert(offset, n2)

        melody.append(m1)
        bass.append(m2)

    # ✅ 插入到 score 中（注意順序）
    score.insert(0, bass)
    score.insert(0, melody)

    # 儲存為 MusicXML 並上傳
    filename = f"melody_{uuid.uuid4().hex}.musicxml"
    score.write('musicxml', fp=filename)

    with open(filename, "rb") as f:
        dbx.files_upload(f.read(), f"/{filename}", mode=dropbox.files.WriteMode.overwrite)

    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(f"/{filename}")
    public_url = shared_link_metadata.url.replace("?dl=0", "?dl=1")

    os.remove(filename)
    return public_url

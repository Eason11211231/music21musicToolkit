from music21 import stream, note, meter, key as m21key
import random
import dropbox
import os
import uuid

DROPBOX_ACCESS_TOKEN = "你的 token 放這裡"
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def generate_melody(style, key_str, time_signature, measures=8):
    score = stream.Score()

    # 調性 & 拍號
    k = m21key.Key(key_str)
    ts = meter.TimeSignature(time_signature)

    # 建立兩個獨立聲部
    melody = stream.Part()
    melody.id = "melody"
    melody.append(k)
    melody.append(ts)

    bass = stream.Part()
    bass.id = "bass"
    bass.append(k)
    bass.append(ts)

    # 產生旋律 & 低音音符
    scale_pitches = k.getPitches()

for _ in range(measures):
    m1 = stream.Measure()
    m2 = stream.Measure()

    for _ in range(4):  # 每拍都產生旋律與低音
        # 旋律音
        pitch_m = random.choice(scale_pitches)
        n1 = note.Note(pitch_m)
        n1.quarterLength = 1.0
        m1.append(n1)

        # 低音音（下八度）
        pitch_b = random.choice(scale_pitches).transpose(-12)
        n2 = note.Note(pitch_b)
        n2.quarterLength = 1.0
        m2.append(n2)

    melody.append(m1)
    bass.append(m2)


    score.append(melody)
    score.append(bass)

    # 儲存並上傳到 Dropbox
    filename = f"melody_{uuid.uuid4().hex}.musicxml"
    score.write('musicxml', fp=filename)

    with open(filename, "rb") as f:
        dbx.files_upload(f.read(), f"/{filename}", mode=dropbox.files.WriteMode.overwrite)

    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(f"/{filename}")
    public_url = shared_link_metadata.url.replace("?dl=0", "?dl=1")

    os.remove(filename)
        return public_url

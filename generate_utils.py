from music21 import stream, note, meter, key as m21key, instrument
import random
import dropbox
import os
import uuid

DROPBOX_ACCESS_TOKEN = "sl.xxxxx.你的_token"
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def generate_melody(style, key_str, time_signature, measures=8):
    score = stream.Score()

    try:
        k = m21key.Key(key_str)
    except:
        k = m21key.Key("C")

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
    bass.append(instrument.Cello())
    bass.append(k)
    bass.append(ts)

    scale_pitches = k.getPitches()

    for _ in range(measures):
        m1 = stream.Measure()
        m2 = stream.Measure()

        for i in range(4):
            offset = i * 1.0

            pitch_m = random.choice(scale_pitches)
            n1 = note.Note(pitch_m)
            n1.quarterLength = 1.0
            m1.insert(offset, n1)

            pitch_b = random.choice(scale_pitches).transpose(-12)
            n2 = note.Note(pitch_b)
            n2.quarterLength = 1.0
            m2.insert(offset, n2)

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
    return public_url

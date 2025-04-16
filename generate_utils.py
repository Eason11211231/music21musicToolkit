from music21 import stream, note, meter, key as m21key
import random

def generate_melody(style, key_str, time_signature, measures=8):
    melody = stream.Part()

    # 加上調號
    try:
        k = m21key.Key(key_str)
        melody.append(k)
    except:
        melody.append(m21key.Key("C"))

    # 加上拍號
    try:
        ts = meter.TimeSignature(time_signature)
        melody.append(ts)
    except:
        melody.append(meter.TimeSignature("4/4"))

    # 簡單旋律產生（根據音階隨機走音）
    scale_pitches = k.getPitches() if 'k' in locals() else m21key.Key("C").getPitches()
    for _ in range(measures):
        m = stream.Measure()
        for _ in range(ts.numerator):
            pitch = random.choice(scale_pitches)
            n = note.Note(pitch)
            n.quarterLength = 1
            m.append(n)
        melody.append(m)

    return melody.write('musicxml')

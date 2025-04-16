from music21 import stream, note, meter, key as m21key
import random

# 節奏型庫
melody_rhythm_pool = [
    [0.5, 0.5, 1.0, 1.0],
    [0.25, 0.75, 1.0, 1.0],
    [0.5, 0.5, 0.5, 0.5, 1.0],
]

def insert_grace_note(pitch):
    g = note.Note(pitch)
    g.quarterLength = 0.25
    g.stemDirection = 'up'
    g.style.size = 75  # 視覺上當裝飾音
    return g

def generate_melody_part(k, ts, measures):
    melody = stream.Part()
    melody.append(k)
    melody.append(ts)

    scale_pitches = k.getPitches()
    for _ in range(measures):
        m = stream.Measure()
        rhythm = random.choice(melody_rhythm_pool)
        for dur in rhythm:
            pitch = random.choice(scale_pitches)
            # 加裝飾音（10% 機率）
            if random.random() < 0.1:
                m.append(insert_grace_note(random.choice(scale_pitches)))
            n = note.Note(pitch)
            n.quarterLength = dur
            m.append(n)
        melody.append(m)
    return melody

def generate_bass_part(k, ts, measures):
    bass = stream.Part()
    bass.append(k)
    bass.append(ts)

    scale_pitches = k.getPitches('C3', 'C4')  # 比旋律低一個八度
    for _ in range(measures):
        m = stream.Measure()
        root = scale_pitches[0]  # 根音
        n = note.Note(root)
        n.quarterLength = ts.barDuration.quarterLength
        n.stemDirection = 'down'
        m.append(n)
        bass.append(m)
    return bass

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

    melody = generate_melody_part(k, ts, measures)
    bass = generate_bass_part(k, ts, measures)

    score.append(melody)
    score.append(bass)

    return score.write('musicxml')

from music21 import note, pitch, stream, duration
import random

# 🎹 取得全鋼琴音域的 Pitch（A0 到 C8）
def get_full_piano_pitch_list():
    pitches = []
    for midi_num in range(21, 109):  # A0 ~ C8
        try:
            p = pitch.Pitch()
            p.midi = midi_num
            pitches.append(p)
        except:
            continue
    return pitches

# ⏱ 支援附點音符的節奏生成
def get_random_duration():
    patterns = [
        ('quarter', 0),   # 四分音符
        ('quarter', 1),   # 附點四分
        ('eighth', 0),    # 八分音符
        ('eighth', 1),    # 附點八分
        ('half', 0),      # 二分音符
        ('half', 1)       # 附點二分
    ]
    dur_type, dots = random.choice(patterns)
    d = duration.Duration(dur_type)
    d.dots = dots
    return d

# 🎵 建立一個 Note（可指定 Pitch）
def create_random_note(pitch_obj=None):
    if pitch_obj is None:
        pitch_obj = random.choice(get_full_piano_pitch_list())
    dur = get_random_duration()
    n = note.Note()
    n.pitch = pitch_obj
    n.duration = dur
    return n

# 🎶 建立一段旋律（可選 step 或 jump）
def create_phrase(length=16, move_style="step"):
    all_pitches = get_full_piano_pitch_list()
    phrase = stream.Part()
    current_pitch = random.choice(all_pitches)

    for _ in range(length):
        if move_style == "step":
            steps = random.choice([-2, -1, 0, 1, 2])
        else:  # jump
            steps = random.choice([-12, -7, -5, 5, 7, 12])

        next_midi = max(21, min(108, current_pitch.midi + steps))
        current_pitch = pitch.Pitch()
        current_pitch.midi = next_midi
        n = create_random_note(current_pitch)
        phrase.append(n)

    return phrase
from music21 import meter

def create_measured_phrase(length=4, time_signature="4/4"):
    ts = meter.TimeSignature(time_signature)
    part = stream.Part()

    for i in range(length):
        m = stream.Measure(number=i+1)
        m.timeSignature = ts
        total_beat = 0.0

        while total_beat < ts.barDuration.quarterLength:
            remaining = ts.barDuration.quarterLength - total_beat
            if remaining >= 1.0:
                dur = duration.Duration(1.0)
            else:
                dur = duration.Duration(remaining)

            n = note.Note(random.choice(['C4', 'D4', 'E4', 'F4', 'G4']))
            n.duration = dur
            n.addLyric(f"M: {i+1}")
            m.append(n)

            total_beat += dur.quarterLength
            total_beat = round(total_beat, 5)

        part.append(m)

    return part

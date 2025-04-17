from music21 import note, pitch, stream, duration
import random

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

def get_random_duration():
    durations = [0.25, 0.5, 1.0, 1.5, 2.0]
    return duration.Duration(random.choice(durations))

def create_random_note(pitch_obj=None):
    if pitch_obj is None:
        pitch_obj = random.choice(get_full_piano_pitch_list())
    dur = get_random_duration()
    n = note.Note()
    n.pitch = pitch_obj
    n.duration = dur
    return n

def create_phrase(length=16, move_style="step"):
    all_pitches = get_full_piano_pitch_list()
    phrase = stream.Part()
    current_pitch = random.choice(all_pitches)

    for _ in range(length):
        if move_style == "step":
            steps = random.choice([-2, -1, 0, 1, 2])
        else:
            steps = random.choice([-12, -7, -5, 5, 7, 12])

        next_midi = max(21, min(108, current_pitch.midi + steps))
        current_pitch = pitch.Pitch()
        current_pitch.midi = next_midi
        n = create_random_note(current_pitch)
        phrase.append(n)

    return phrase

import random

def bassline():
    VELOCITY=40
    while True:
        yield [(36, 60)], 1.6
        yield [(48, VELOCITY)], 1.4
        yield [(43, 60)], 1.6
        yield [(43, VELOCITY)], 1.4

def tenor():
    VELOCITY=40
    while True:
        yield [], 0.6
        yield [(55, VELOCITY), (60, VELOCITY), (64, VELOCITY)], 1
        yield [], 0.4
        yield [(55, VELOCITY), (60, VELOCITY), (64, VELOCITY)], 1
        yield [], 0.6
        yield [(53, VELOCITY), (58, VELOCITY), (62, VELOCITY)], 1
        yield [], 0.4
        yield [(53, VELOCITY), (58, VELOCITY), (62, VELOCITY)], 1

def melody(seed: int=0):
    VELOCITY=80
    random.seed(seed) # consistent randomness for debugging
    notes = [60, 62, 64, 65, 67, 69, 70, 72, 74, 76, 77, 79, 81, 82, 84]
    last_note_index = 4 # gotta start somewhere
    yield [], 12
    note_count = 0
    while True:
        offset = random.choice([-2, -1, -1, 0, 1, 1, 2])
        if 0 <= last_note_index + offset < len(notes):
            last_note_index = last_note_index + offset
            yield [(notes[last_note_index], VELOCITY)], [0.6,0.4][note_count % 2]
            note_count += 1

parts=[bassline(), tenor(), melody()]

BPM=144

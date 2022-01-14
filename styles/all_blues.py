import random

progression_offsets = [0, 0, 0, 0, 5, 5, 0, 0, 7, 5, 0, 0]

def swing(generator):
    note_start = 0
    while True:
        notes, original_duration = next(generator)
        note_end = note_start + original_duration
        new_duration = original_duration
        if note_end % 1 == 0.5:
            new_duration += 0.1 # 60% swing
        if note_start % 1 == 0.5:
            new_duration -= 0.1
        yield notes, new_duration
        note_start = note_end

def bassline():
    VELOCITY=40
    for _ in range(2): # intro
        yield [(43, VELOCITY)], 1.5
        yield [(50, VELOCITY)], 0.5
        yield [(52, VELOCITY)], 0.5
        yield [(50, VELOCITY)], 0.5
        yield [(53, VELOCITY)], 1.5
        yield [(50, VELOCITY)], 0.5
        yield [(52, VELOCITY)], 0.5
        yield [(50, VELOCITY)], 0.5
    while True:
        for offset in progression_offsets:
            yield [(43 + offset, VELOCITY)], 1.5
            yield [(50 + offset, VELOCITY)], 0.5
            yield [(52 + offset, VELOCITY)], 0.5
            yield [(50 + offset, VELOCITY)], 0.5
            yield [(53 + offset, VELOCITY)], 1.5
            yield [(50 + offset, VELOCITY)], 0.5
            yield [(52 + offset, VELOCITY)], 0.5
            yield [(50 + offset, VELOCITY)], 0.5

def tenor():
    VELOCITY=40
    for _ in range(2): # intro
        yield [(59, VELOCITY), (53, VELOCITY), (62, VELOCITY)], 2
        yield [(55, VELOCITY), (64, VELOCITY), (60, VELOCITY)], 1
        yield [(57, VELOCITY), (65, VELOCITY), (62, VELOCITY)], 2
        yield [(55, VELOCITY), (60, VELOCITY), (64, VELOCITY)], 1
    while True:
        for _ in range(4):
            yield [(59, VELOCITY), (53, VELOCITY), (62, VELOCITY)], 2
            yield [(55, VELOCITY), (64, VELOCITY), (60, VELOCITY)], 1
            yield [(57, VELOCITY), (65, VELOCITY), (62, VELOCITY)], 2
            yield [(55, VELOCITY), (60, VELOCITY), (64, VELOCITY)], 1
        for _ in range(2):
            yield [(52, VELOCITY), (62, VELOCITY), (58, VELOCITY)], 2
            yield [(58, VELOCITY), (64, VELOCITY), (55, VELOCITY)], 1
            yield [(58, VELOCITY), (55, VELOCITY), (65, VELOCITY)], 2
            yield [(58, VELOCITY), (64, VELOCITY), (55, VELOCITY)], 1
        for _ in range(2):
            yield [(59, VELOCITY), (53, VELOCITY), (62, VELOCITY)], 2
            yield [(55, VELOCITY), (64, VELOCITY), (60, VELOCITY)], 1
            yield [(57, VELOCITY), (65, VELOCITY), (62, VELOCITY)], 2
            yield [(55, VELOCITY), (60, VELOCITY), (64, VELOCITY)], 1
        for _ in range(1):
            yield [(54, VELOCITY), (64, VELOCITY), (60, VELOCITY)], 2
            yield [(60, VELOCITY), (66, VELOCITY), (57, VELOCITY)], 1
            yield [(60, VELOCITY), (57, VELOCITY), (67, VELOCITY)], 2
            yield [(60, VELOCITY), (66, VELOCITY), (57, VELOCITY)], 1
        for _ in range(1):
            yield [(52, VELOCITY), (62, VELOCITY), (58, VELOCITY)], 2
            yield [(58, VELOCITY), (64, VELOCITY), (55, VELOCITY)], 1
            yield [(58, VELOCITY), (55, VELOCITY), (65, VELOCITY)], 2
            yield [(58, VELOCITY), (64, VELOCITY), (55, VELOCITY)], 1
        for _ in range(2):
            yield [(59, VELOCITY), (53, VELOCITY), (62, VELOCITY)], 2
            yield [(55, VELOCITY), (64, VELOCITY), (60, VELOCITY)], 1
            yield [(57, VELOCITY), (65, VELOCITY), (62, VELOCITY)], 2
            yield [(55, VELOCITY), (60, VELOCITY), (64, VELOCITY)], 1

def melody(seed: int=0):
    VELOCITY=80
    random.seed(seed) # consistent randomness for debugging
    notes = [67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84]
    last_note_index = 4 # gotta start somewhere
    yield [], 12
    note_count = 0
    while True:
        offset = random.choice([-2, -1, -1, 0, 1, 1, 2])
        if 0 <= last_note_index + offset < len(notes):
            last_note_index = last_note_index + offset
            yield [(notes[last_note_index], VELOCITY)], [0.6,0.4][note_count % 2]
            note_count += 1

parts=[swing(bassline()), tenor(), melody()]

BPM=120

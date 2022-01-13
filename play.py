import time
import fluidsynth
import random

fs = fluidsynth.Synth()
fs.start()

def bassline():
    VELOCITY=40
    while True:
        yield [(36, VELOCITY)], 2
        yield [(38, VELOCITY)], 2

def tenor():
    VELOCITY=40
    while True:
        yield [], 0.5
        yield [(52, VELOCITY), (55, VELOCITY), (59, VELOCITY)], 0.25
        yield [], 0.75
        yield [(52, VELOCITY), (55, VELOCITY), (59, VELOCITY)], 0.25
        yield [], 0.75
        yield [(53, VELOCITY), (57, VELOCITY), (60, VELOCITY)], 0.25
        yield [], 0.75
        yield [(53, VELOCITY), (57, VELOCITY), (60, VELOCITY)], 0.25
        yield [], 0.25

def melody():
    VELOCITY=80
    random.seed(0) # consistent randomness for debugging
    # a premade bit of melody
    # while True:
    #     for note in "71 72 71 72 71 67 64 67 69 65 62 69 67 64 57 59".split():
    #         yield [(int(note), 100)], 0.25
    #     yield [(55, 100)], 4
    notes = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84]
    last_note_index = 4 # gotta start somewhere
    yield [(notes[last_note_index], 100)], 0.5
    while True:
        offset = random.choice([-2, -1, -1, 0, 1, 1, 2])
        if 0 <= last_note_index + offset < len(notes):
            last_note_index = last_note_index + offset
            yield [(notes[last_note_index], VELOCITY)], 0.25

BPM=60

def play(notes_stream):
    while True:
        notes = next(notes_stream)
        for note in notes[0]:
            fs.noteon(0, note[0], note[1])
        time.sleep(notes[1] * 60/BPM)
        for note in notes[0]:
            fs.noteoff(0, note[0])

# available from https://sites.google.com/site/soundfonts4u/
sfid = fs.sfload("soundfonts/Essential Keys-sforzando-v9.6.sf2")
fs.program_select(0, sfid, 0, 8)

import threading # hacks, TODO: as generator?
bass_thread = threading.Thread(target=play, args=(bassline(),))
bass_thread.start()
tenor_thread = threading.Thread(target=play, args=(tenor(),))
tenor_thread.start()
melody_thread = threading.Thread(target=play, args=(melody(),))
melody_thread.start()

bass_thread.join()

fs.delete()

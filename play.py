import time
from typing import List
import fluidsynth
import random
import functools
import heapq

# TODO: typing

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

@functools.total_ordering
class Event:
    event_type: str
    start_time: float
    key_id: int
    velocity: int
    def __init__(self, event_type, start_time, key_id, velocity):
        self.event_type = event_type
        self.start_time = start_time
        self.key_id = key_id
        self.velocity = velocity
    def __lt__(self, other):
        return self.start_time < other.start_time if self.start_time != other.start_time else self.event_type < other.event_type
    def __str__(self) -> str:
        return f"{self.event_type}@{self.start_time:.3f}: {self.key_id}@{self.velocity}"

BPM=60
DEBUG=False

# TODO: I think fluidsynth.Sequencer would make a lot of this easier?
# TODO: synchronize with real time; could be free with fluidsynth.Sequencer
def play(*parts):
    q: List(Event) = [] # empty heap
    current_time = 0
    searched_until = 0
    parts = [[part, 0] for part in parts] # add a time counter to each part
    while True:
        # replenish queue if needed
        if searched_until < current_time + 10: # 10 is an arbitrarily chosen search increment
            for part in parts:
                while part[1] < searched_until + 10: # 10 from above
                    new_notes, delay_after = next(part[0]) # get the next note
                    for note in new_notes:
                        heapq.heappush(q, Event("noteon", part[1], note[0], note[1]))
                        heapq.heappush(q, Event("noteoff", part[1] + delay_after, note[0], note[1]))
                    part[1] += delay_after
            searched_until += 10
        # TODO: remove (debug)
        if q[0].start_time < current_time:
            raise RuntimeError("note happened in past, should not happen")
        # play notes we're ready for
        while q[0].start_time == current_time:
            n = heapq.heappop(q)
            if n.event_type == "noteon":
                if DEBUG:
                    print(f"fs.noteon(0, {n.key_id}, {n.velocity})")
                fs.noteon(0, n.key_id, n.velocity)
            elif n.event_type == "noteoff":
                if DEBUG:
                    print(f"fs.noteoff(0, {n.key_id})")
                fs.noteoff(0, n.key_id)
        if DEBUG:
            print(f"time.sleep({(q[0].start_time - current_time)})")
        time.sleep((q[0].start_time - current_time))
        current_time = q[0].start_time

# available from https://sites.google.com/site/soundfonts4u/
sfid = fs.sfload("soundfonts/Essential Keys-sforzando-v9.6.sf2")
fs.program_select(0, sfid, 0, 8)

try:
    play(bassline(), tenor(), melody())
except KeyboardInterrupt:
    pass

fs.delete()

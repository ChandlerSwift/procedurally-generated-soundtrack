import time
from typing import List
import fluidsynth
import functools
import heapq
import os

# TODO: typing

WAV_EXPORT=False
if os.environ.get("WAV_EXPORT", "") != "":
    WAV_BEATS=int(os.environ.get("WAV_BEATS", "32"))
    WAV_EXPORT=True

    import wave
    import numpy
    import sys
    import io
    buf = io.BytesIO()
    w: wave.Wave_write = wave.open(buf, "wb")
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(44100)

fs = fluidsynth.Synth()
if not WAV_EXPORT:
    fs.start()

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

DEBUG=False

# TODO: I think fluidsynth.Sequencer would make a lot of this easier?
# TODO: synchronize with real time; could be free with fluidsynth.Sequencer
def play(*parts, BPM: int):
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
        if WAV_EXPORT:
            samples = fs.get_samples(int(44100 * ((q[0].start_time - current_time) * 60/BPM)))
            w.writeframes(samples.astype(numpy.int16).tobytes())
        else:
            time.sleep((q[0].start_time - current_time) * 60/BPM)
        current_time = q[0].start_time
        if WAV_EXPORT and current_time > WAV_BEATS: # wrap it up
            samples = fs.get_samples(44100 * 2)
            w.writeframes(samples.astype(numpy.int16).tobytes())
            for e in q:
                if e.event_type == "noteoff":
                    fs.noteoff(0, e.key_id)
            break

# available from https://sites.google.com/site/soundfonts4u/
sfid = fs.sfload("soundfonts/Essential Keys-sforzando-v9.6.sf2")
fs.program_select(0, sfid, 0, 8)

import sys
if len(sys.argv) > 1 and sys.argv[1] != "":
    style = sys.argv[1]
else:
    style = "peaceful"

import importlib
style = importlib.import_module(f"styles.{style}")

try:
    play(*style.parts, BPM=style.BPM)
except KeyboardInterrupt:
    pass

fs.delete()

if WAV_EXPORT:
    sys.stdout.buffer.write(buf.getvalue())

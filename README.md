# procedurally-generated-soundtrack

Built for [cavetown](https://github.com/toxicglados/cavetown)

### Installation and use

```sh
pip install -r requirements.txt
python play.py
```

### Sample output

Style | FLAC | MP3
--|--|--|
All Blues | [all_blues.flac](https://github.com/ChandlerSwift/procedurally-generated-soundtrack/raw/main/samples/all_blues.flac) | [all_blues.mp3](https://github.com/ChandlerSwift/procedurally-generated-soundtrack/raw/main/samples/all_blues.mp3)
Jazz Waltz | [jazz_waltz.flac](https://github.com/ChandlerSwift/procedurally-generated-soundtrack/raw/main/samples/jazz_waltz.flac) | [jazz_waltz.mp3](https://github.com/ChandlerSwift/procedurally-generated-soundtrack/raw/main/samples/jazz_waltz.mp3)
Peaceful (Double time melody) | [peaceful_double_time_melody.flac](https://github.com/ChandlerSwift/procedurally-generated-soundtrack/raw/main/samples/peaceful_double_time_melody.flac) | [peaceful_double_time_melody.mp3](https://github.com/ChandlerSwift/procedurally-generated-soundtrack/raw/main/samples/peaceful_double_time_melody.mp3)
Peaceful | [peaceful.flac](https://github.com/ChandlerSwift/procedurally-generated-soundtrack/raw/main/samples/peaceful.flac) | [peaceful.mp3](https://github.com/ChandlerSwift/procedurally-generated-soundtrack/raw/main/samples/peaceful.mp3)

### `parse_keys.py`

A helper script to simplify generating notes with the help of a MIDI keyboard.

Find your MIDI port (`aseqdump` is part of `alsa-utils` on Arch):
```
% aseqdump -l
 Port    Client name                      Port name
  0:0    System                           Timer
  0:1    System                           Announce
 14:0    Midi Through                     Midi Through Port-0
 24:0    PCR                              PCR MIDI
 24:1    PCR                              PCR 1
 24:2    PCR                              PCR 2
% 
```

I'm using `24:1`. Verify you get input by pressing some keys:
```
% aseqdump -p 24:1
Waiting for data. Press Ctrl+C to end.
Source  Event                  Ch  Data
 24:1   Note on                 8, note 62, velocity 49
 24:1   Note off                8, note 62, velocity 80
 24:1   Note on                 8, note 64, velocity 37
 24:1   Note off                8, note 64, velocity 59
 24:1   Note on                 8, note 65, velocity 50
 24:1   Note off                8, note 65, velocity 62
 24:1   Note on                 8, note 67, velocity 47
 24:1   Note off                8, note 67, velocity 31
 24:1   Note on                 8, note 64, velocity 51
 24:1   Note off                8, note 64, velocity 50
 24:1   Note on                 8, note 60, velocity 48
 24:1   Note off                8, note 60, velocity 40
 24:1   Note on                 8, note 62, velocity 38
 24:1   Note off                8, note 62, velocity 53
^C
% 
```

Then, pass the output of `aseqdump` to `parse_keys.py` (here's part of a blues):

```
% aseqdump -p 24:1 | python parse_keys.py
yield [(64, VELOCITY), (58, VELOCITY)], 1
yield [(63, VELOCITY), (57, VELOCITY)], 1
yield [(64, VELOCITY), (58, VELOCITY)], 1
yield [(65, VELOCITY), (59, VELOCITY)], 1
yield [(63, VELOCITY), (57, VELOCITY)], 1
yield [(58, VELOCITY), (64, VELOCITY)], 1
```

This is valid Python that can be put in one of the generator functions (just
define `VELOCITY` and edit the durations).

```python
def tenor():
    while True:
        yield [(64, VELOCITY), (58, VELOCITY)], 8
        yield [(63, VELOCITY), (57, VELOCITY)], 4
        yield [(64, VELOCITY), (58, VELOCITY)], 4
        yield [(65, VELOCITY), (59, VELOCITY)], 2
        yield [(63, VELOCITY), (57, VELOCITY)], 2
        yield [(58, VELOCITY), (64, VELOCITY)], 4
```

### Generating samples

```sh
rm samples/*

WAV_EXPORT=true WAV_BEATS=78 python play.py all_blues 2>/dev/null | ffmpeg -i - samples/all_blues.flac 2>/dev/null
WAV_EXPORT=true WAV_BEATS=78 python play.py all_blues 2>/dev/null | ffmpeg -i - samples/all_blues.mp3 2>/dev/null

WAV_EXPORT=true WAV_BEATS=60 python play.py jazz_waltz 2>/dev/null | ffmpeg -i - samples/jazz_waltz.flac 2>/dev/null
WAV_EXPORT=true WAV_BEATS=60 python play.py jazz_waltz 2>/dev/null | ffmpeg -i - samples/jazz_waltz.mp3 2>/dev/null

WAV_EXPORT=true WAV_BEATS=32 python play.py peaceful_double_time_melody 2>/dev/null | ffmpeg -i - samples/peaceful_double_time_melody.flac 2>/dev/null
WAV_EXPORT=true WAV_BEATS=32 python play.py peaceful_double_time_melody 2>/dev/null | ffmpeg -i - samples/peaceful_double_time_melody.mp3 2>/dev/null

WAV_EXPORT=true WAV_BEATS=32 python play.py peaceful 2>/dev/null | ffmpeg -i - samples/peaceful.flac 2>/dev/null
WAV_EXPORT=true WAV_BEATS=32 python play.py peaceful 2>/dev/null | ffmpeg -i - samples/peaceful.mp3 2>/dev/null
```

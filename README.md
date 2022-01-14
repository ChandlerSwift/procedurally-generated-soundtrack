# procedurally-generated-soundtrack

Built for [cavetown](https://github.com/toxicglados/cavetown)

### Installation and use

```sh
pip install -r requirements.txt
python play.py
```

### Sample output
Generated from d51d79e241b12ab0bc5b7a76a4b9b51dab819769.

<audio controls>
  <source src="https://github.com/ChandlerSwift/procedurally-generated-soundtrack/raw/main/samples/sample.flac" type="audio/flac">
  <source src="https://github.com/ChandlerSwift/procedurally-generated-soundtrack/raw/main/samples/sample.ogg" type="audio/ogg">
  <source src="https://github.com/ChandlerSwift/procedurally-generated-soundtrack/raw/main/samples/sample.mp3" type="audio/mpeg">
  <a href="https://github.com/ChandlerSwift/procedurally-generated-soundtrack/raw/main/samples/sample.mp3">Download audio</a>
</audio>

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

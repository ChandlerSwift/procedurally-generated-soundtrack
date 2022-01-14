# https://stackoverflow.com/a/1454400
import fileinput
active_notes = []
for line in fileinput.input():
    if "Waiting for data." in line:
        continue
    if line.split() == ["Source", "Event", "Ch", "Data"]:
        continue
    source, _, event, ch, _, note, _, velocity = line.replace(",", "").split()
    if event == "on":
        active_notes.append(note)
    elif event == "off":
        if len(active_notes) > 0:
            print(f"yield [{', '.join([f'({note}, VELOCITY)' for note in active_notes])}], 1")
            active_notes = []
    else:
        print(f"# unknown event {event}")

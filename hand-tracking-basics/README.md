# Hand Tracking Basics

My first MediaPipe experiment, and the starting point for every other project here. It
draws the 21 hand landmarks and their connections, puts a marker above the wrist, and
shows the FPS.

```bash
cd hand-tracking-basics
python hand_tracking_basic.py   # q to quit
```

MediaPipe numbers the hand landmarks like this. They're useful for writing your own
gestures:

```
 0 wrist        4 thumb tip     8 index tip     12 middle tip    16 ring tip    20 pinky tip
 5 index base   9 middle base  13 ring base     17 pinky base
```

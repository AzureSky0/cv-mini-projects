# Gesture Volume Control

Change your computer's volume by pinching your thumb and index finger in front of the
webcam. **Windows only**, because it uses the Windows audio API through `pycaw`.

| Pinch distance | Volume |
|----------------|--------|
| Fingers touching (≤ 50 px) | 0 % |
| About 100 px apart | 100 % |

```bash
cd volume-control
python volume_control.py     # q to quit
```

- `volume_control.py`: the app (webcam, volume bar, pycaw calls)
- `hand_tracking.py`: a reusable `HandDetector` class built on MediaPipe Hands. Run it on
  its own for a landmark and FPS demo.

> Your volume changes as soon as a hand is in view. Keep your hand out of the frame if you
> don't want that.

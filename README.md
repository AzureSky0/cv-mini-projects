# Computer Vision Mini Projects

Small real-time computer-vision projects I built with **OpenCV** and **MediaPipe** during
my 4th semester (2022), while learning the skills behind my bigger projects.

| Project | What it does | Platform |
|---------|--------------|----------|
| [volume-control](volume-control/) | Change the system volume by pinching your thumb and index finger | Windows |
| [object-detection](object-detection/) | Detect 80 everyday objects live with SSD MobileNet v3 (COCO) | Any |
| [hand-sign-dataset](hand-sign-dataset/) | Collect webcam images of hand signs to train a custom detector | Any |
| [hand-tracking-basics](hand-tracking-basics/) | My first MediaPipe script: 21 hand landmarks and FPS | Any |

## Setup

You need Python 3.9–3.12 and a webcam.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Then go into a project folder and run its script, for example:

```bash
cd object-detection
python object_detection.py
```

Every app quits when you press `q`. Each folder has its own README with details.

Tested on Windows 11 with Python 3.12, mediapipe 0.10.14, OpenCV 5.0 and numpy 2.x.

## Related projects

- **[gesture-virtual-window](https://github.com/AzureSky0/gesture-virtual-window)**: a webcam window you control with hand gestures. It includes
  face recognition and a touch-your-face game.
- **[dementia-face-assistant](https://github.com/AzureSky0/dementia-face-assistant)**: recognises the people around a person with dementia and
  reminds them who each person is.

## License

[MIT](LICENSE) © Akshat Sahu

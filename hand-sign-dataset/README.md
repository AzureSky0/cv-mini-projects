# Hand Sign Dataset Collector

Step 1 of training a custom hand-sign detector for four signs: **hi**, **namaste**, **ok**
and **victory**. The script takes photos of each sign from your webcam.

```bash
cd hand-sign-dataset
python capture_images.py
```

For each sign, you get a 5-second countdown, and then it takes 15 photos 2 seconds apart.
The photos are saved as `dataset/<label>/<label>.<uuid>.jpg`. Change `LABELS` or
`NUM_IMAGES` at the top of the script to collect different signs.

## Full pipeline

1. **Collect** images with `capture_images.py`. ✅ (this script)
2. **Label** them by drawing a box around the hand with
   [labelImg](https://github.com/HumanSignal/labelImg) (`pip install labelImg`, then
   `labelImg`). It saves one Pascal VOC `.xml` file per image.
3. **Split** them into `train/` and `test/` folders. I used about 80/20.
4. **Train** a detector, for example with the TensorFlow Object Detection API, starting from
   a pre-trained SSD MobileNet checkpoint.
5. **Detect** signs live from the webcam.

I completed steps 1–3 (60 labelled images). Training was never finished. The original
dataset isn't included because the photos show my face; `dataset/` is git-ignored for the
same reason.

"""
Hand Sign Dataset Collector

Step 1 of training a custom hand-sign detector: take webcam photos of each sign.

For every label it waits 5 seconds so you can get ready, then takes NUM_IMAGES photos,
2 seconds apart. Images are saved as  dataset/<label>/<label>.<uuid>.jpg
Press q to skip to the next label.

Next steps (see README): label the images with labelImg, split into train/test, then train.
"""

import uuid
from pathlib import Path

import cv2

DATASET_DIR = Path(__file__).resolve().parent / "dataset"
LABELS = ["hi", "namaste", "ok", "victory"]
NUM_IMAGES = 15
GET_READY_MS = 5000
BETWEEN_SHOTS_MS = 2000


def countdown(cap, label, ms):
    """Show the live camera with a 'get ready' message for `ms` milliseconds."""
    steps = ms // 100
    for i in range(steps):
        success, frame = cap.read()
        if not success:
            return
        seconds_left = (steps - i) // 10 + 1
        cv2.putText(frame, f"Get ready: {label} ({seconds_left})", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Capture", frame)
        cv2.waitKey(100)


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Could not open the webcam.")

    for label in LABELS:
        label_dir = DATASET_DIR / label
        label_dir.mkdir(parents=True, exist_ok=True)

        print(f"Collecting images for '{label}'")
        countdown(cap, label, GET_READY_MS)

        for img_num in range(NUM_IMAGES):
            success, frame = cap.read()
            if not success:
                break
            path = label_dir / f"{label}.{uuid.uuid1()}.jpg"
            cv2.imwrite(str(path), frame)
            print(f"  saved {path.name} ({img_num + 1}/{NUM_IMAGES})")

            cv2.putText(frame, f"{label}: {img_num + 1}/{NUM_IMAGES}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Capture", frame)
            if cv2.waitKey(BETWEEN_SHOTS_MS) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Done. Images are in {DATASET_DIR}")


if __name__ == "__main__":
    main()

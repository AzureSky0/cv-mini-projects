"""
Real-time Object Detection

Detects the 80 COCO object classes (person, bottle, phone, car, ...) in your webcam feed
using the pre-trained SSD MobileNet v3 model through OpenCV's DNN module.
Press q to quit.
"""

from pathlib import Path

import cv2

MODEL_DIR = Path(__file__).resolve().parent / "model"
CLASS_FILE = MODEL_DIR / "coco.names"
CONFIG_PATH = MODEL_DIR / "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
WEIGHTS_PATH = MODEL_DIR / "frozen_inference_graph.pb"

CONFIDENCE_THRESHOLD = 0.5


def load_model():
    net = cv2.dnn_DetectionModel(str(WEIGHTS_PATH), str(CONFIG_PATH))
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    return net


def main():
    class_names = CLASS_FILE.read_text().strip().split("\n")
    net = load_model()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, img = cap.read()
        if not success:
            break

        class_ids, confidences, boxes = net.detect(img, confThreshold=CONFIDENCE_THRESHOLD)

        for class_id, confidence, box in zip(class_ids.flatten() if len(class_ids) else [],
                                             confidences.flatten() if len(confidences) else [],
                                             boxes):
            x, y = box[0], box[1]
            label = class_names[class_id - 1] if 0 < class_id <= len(class_names) else str(class_id)
            cv2.rectangle(img, box, (0, 225, 0), 2)
            cv2.putText(img, f"{label} {confidence * 100:.0f}%", (x + 10, y + 30),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        cv2.imshow("Object detection (press q to quit)", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

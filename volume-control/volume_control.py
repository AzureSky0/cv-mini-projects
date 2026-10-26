"""
Gesture Volume Control (Windows only)

Control the system volume by pinching: the distance between your thumb tip and your
index fingertip sets the volume. Fingers together = 0 %, about 100 px apart = 100 %.
Press q to quit.
"""

import sys

import cv2
import numpy as np

from hand_tracking import HandDetector

if sys.platform != "win32":
    sys.exit("Volume control uses the Windows audio API (pycaw) and only works on Windows.")

from ctypes import POINTER, cast  # noqa: E402

from comtypes import CLSCTX_ALL  # noqa: E402
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # noqa: E402

MIN_DIST, MAX_DIST = 50, 100  # pinch distance in pixels mapped to 0 % .. 100 %


def get_volume_control():
    speakers = AudioUtilities.GetSpeakers()
    if hasattr(speakers, "EndpointVolume"):  # pycaw 2025+
        return speakers.EndpointVolume
    interface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)  # older pycaw
    return cast(interface, POINTER(IAudioEndpointVolume))


def main():
    volume = get_volume_control()
    detector = HandDetector(detection_confidence=0.7)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 870)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

    vol_percent = volume.GetMasterVolumeLevelScalar() * 100

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1)

        img = detector.find_hands(img, draw=False)
        lm_list = detector.find_hand_pos(img, draw=False)

        if lm_list:
            x1, y1 = lm_list[4][1:]   # thumb tip
            x2, y2 = lm_list[8][1:]   # index fingertip
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.line(img, (x1, y1), (x2, y2), (125, 250, 0), 3)
            cv2.circle(img, (x1, y1), 7, (125, 125, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 7, (125, 125, 0), cv2.FILLED)

            length = detector.find_distance(4, 8, lm_list)
            vol_percent = float(np.interp(length, [MIN_DIST, MAX_DIST], [0, 100]))
            volume.SetMasterVolumeLevelScalar(vol_percent / 100, None)

            at_limit = length <= MIN_DIST or length >= MAX_DIST
            cv2.circle(img, (cx, cy), 7, (250, 0, 250) if at_limit else (0, 225, 0), cv2.FILLED)

        # Volume bar
        bar_top = int(np.interp(vol_percent, [0, 100], [300, 100]))
        cv2.rectangle(img, (50, 100), (65, 300), (0, 255, 0), 3)
        cv2.rectangle(img, (50, bar_top), (65, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f"{int(vol_percent)} %", (40, 60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 250), 2)

        cv2.imshow("Gesture volume control (press q to quit)", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

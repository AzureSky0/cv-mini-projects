"""Hand tracking helper built on MediaPipe Hands.

Usage:
    detector = HandDetector()
    img = detector.find_hands(img)        # must be called first on every frame
    lm_list = detector.find_hand_pos(img) # [[id, x, y], ...] for the 21 landmarks

Run this file directly for a webcam demo:  python hand_tracking.py
"""

import math
import time

import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self.mpDraws = mp.solutions.drawing_utils
        self.result = None

    def find_hands(self, img, draw=True):
        """Detect hands in a BGR frame and optionally draw the hand skeleton."""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(img_rgb)

        if draw and self.result.multi_hand_landmarks:
            for hand_lms in self.result.multi_hand_landmarks:
                self.mpDraws.draw_landmarks(img, hand_lms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_hand_pos(self, img, hand_no=0, draw=True):
        """Return pixel positions [[id, x, y], ...] of one hand's landmarks (empty list if none)."""
        if self.result is None:
            raise RuntimeError("Call find_hands(img) before find_hand_pos(img).")

        lm_list = []
        hands = self.result.multi_hand_landmarks
        if hands and hand_no < len(hands):
            h, w, _ = img.shape
            for lm_id, lm in enumerate(hands[hand_no].landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([lm_id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (150, 150, 150), cv2.FILLED)
        return lm_list

    @staticmethod
    def find_distance(p1, p2, lm_list):
        """Pixel distance between two landmarks, or None if no hand was found."""
        if not lm_list:
            return None
        x1, y1 = lm_list[p1][1:]
        x2, y2 = lm_list[p2][1:]
        return math.hypot(x2 - x1, y2 - y1)

    @staticmethod
    def find_distance_for_cam(lm_list):
        """Distance between knuckles 5 and 9. Bigger value = hand closer to the camera."""
        return HandDetector.find_distance(5, 9, lm_list)


def main():
    p_time = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.find_hands(img)
        lm_list = detector.find_hand_pos(img)

        cam_distance = detector.find_distance_for_cam(lm_list)
        if cam_distance and cam_distance > 40:
            print("Hand in range", int(cam_distance))

        c_time = time.time()
        fps = 1 / (c_time - p_time) if p_time else 0
        p_time = c_time
        cv2.putText(img, f"FPS {int(fps)}", (20, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 250), 2)

        cv2.imshow("Hand tracking (press q to quit)", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

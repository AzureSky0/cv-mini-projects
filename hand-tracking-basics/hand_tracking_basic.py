"""
Hand Tracking Basics

My first MediaPipe script: draws the 21 hand landmarks and a marker above the wrist,
plus an FPS counter. Press q to quit.
"""

import time

import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def main():
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands()
    p_time = 0

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1)

        result = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if result.multi_hand_landmarks:
            h, w, _ = img.shape
            for hand_lms in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

                wrist = hand_lms.landmark[0]
                cx, cy = int(wrist.x * w), int(wrist.y * h)
                cv2.circle(img, (cx, cy - 50), 15, (150, 150, 150), cv2.FILLED)

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

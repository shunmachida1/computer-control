import cv2
import mediapipe as mp
import pyautogui
import utils
from actions import ActionDetector

webcam = cv2.VideoCapture(0)

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
     max_num_hands = 1,
     min_detection_confidence = 0.7,
     min_tracking_confidence = 0.7
)

action = ActionDetector()

#Smoothing
prev_x, prev_y = 0, 0
smooth = 0.2

pinch_down = False

width, height = pyautogui.size()

scrollmode = False

while True:
    success, frame = webcam.read()

    if not success:
        break

    h, w, c = frame.shape

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frameRGB)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            
            action.detect_click(hand)

            action.move(hand)

            action.detect_scroll(hand)
            
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            
    utils.show_fps(frame)

    cv2.imshow("Action Controlled Computer", frame)

    if cv2.waitKey(10) & 0xff == ord('q'):
            break

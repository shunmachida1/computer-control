import cv2
import mediapipe as mp
import pyautogui
import utils
import actions

webcam = cv2.VideoCapture(0)

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
     max_num_hands = 1,
     min_detection_confidence = 0.7,
     min_tracking_confidence = 0.7
)

actions = actions.ActionDetector()

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
            
            if actions.click():
                pyautogui.click()

            #Track position of pointer

            pointerx = hand.landmark[8].x
            pointerx = 1-pointerx
            pointery = hand.landmark[8].y

            new_x = pointerx * width
            new_y = pointery * height

            smooth_x = prev_x + (new_x - prev_x) * smooth
            smooth_y = prev_y + (new_y - prev_y) * smooth

            pyautogui.moveTo(int(smooth_x), int(smooth_y))

            prev_x = smooth_x
            prev_y = smooth_y

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            #Scrolling using middle and thumb modes

            middlex = hand.landmark[12].x
            middley = hand.landmark[12].y

            scrolldistance = utils.find_distance(hand, 12, 4)

            if scrolldistance < 0.08:
                if not scrollmode:
                    pyautogui.scroll(-50)
                    print("Scroll")
                    scrollmode = True

            else:
                scrollmode = False


    utils.show_fps(frame)

    cv2.imshow("bruh", frame)

    if cv2.waitKey(10) & 0xff == ord('q'):
            break

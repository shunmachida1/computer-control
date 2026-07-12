import cv2
import mediapipe as mp
import time
import math
import pyautogui

webcam = cv2.VideoCapture(0)

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
     max_num_hands = 1,
     min_detection_confidence = 0.7,
     min_tracking_confidence = 0.7
)

#FPS
pTime = 0
cTime = 0

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
            #for id, lm in enumerate(hand.landmark):
                
                #pw, ph = (w * lm.x), (h * lm.y)

                #print(f"{id}: {int(pw)}, {int(ph)}")

            thumby = hand.landmark[4].y
            pinkyy = hand.landmark[20].y

            thumbx = hand.landmark[4].x
            pinkyx = hand.landmark[20].x

            clickdistance = math.sqrt((thumby - pinkyy)**2 + (thumbx - pinkyx)**2)

            #Click when Pinched

            if clickdistance < 0.07:
                if not pinch_down:
                    pyautogui.click()
                    pinch_down = True
                    print("Touching")

            else:
                pinch_down = False

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

            scrolldistance = math.sqrt((thumby - middley)**2 + (thumbx - middlex)**2)

            if scrolldistance < 0.08:
                if not scrollmode:
                    pyautogui.scroll(-50)
                    print("Scroll")
                    scrollmode = True

            else:
                scrollmode = False


    #Show FPS

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 2)


    cv2.imshow("bruh", frame)

    if cv2.waitKey(10) & 0xff == ord('q'):
            break

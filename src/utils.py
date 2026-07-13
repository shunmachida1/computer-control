import math
import time
import cv2

def find_distance(hand, id1, id2):

    x_distance = hand.landmark[id1].x - hand.landmark[id2].x
    y_distance = hand.landmark[id1].y - hand.landmark[id2].y

    distance = math.sqrt((x_distance ** 2) + (y_distance ** 2))

    return distance


def show_fps(frame):
    pTime = 0
    cTime = 0

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 2)
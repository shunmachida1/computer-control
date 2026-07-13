import mediapipe as mp
import pyautogui
import utils

class ActionDetector:
    def __init__(self):
        pass

    def click(hand):

        clickdistance = utils.find_distance(hand, 4, 20)

        if clickdistance < 0.07:
            if not pinch_down:
                pyautogui.click()
                pinch_down = True
                print("Touching")

            else:
                pinch_down = False
                
        return False

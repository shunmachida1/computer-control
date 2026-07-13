import mediapipe as mp
import pyautogui
import utils as utils

class ActionDetector:
    def __init__(self):
        self.pinch_down = False
        self.scrollmode = False
        self.screen_x, self.screen_y = pyautogui.size()

    def move(self, hand):
        pointer_x = hand.landmark[8].x
        pointer_x = 1-pointer_x
        pointer_y = hand.landmark[8].y

        mouse_pos_x = pointer_x * self.screen_x
        mouse_pos_y = pointer_y * self.screen_y

        pyautogui.moveTo(int(mouse_pos_x), int(mouse_pos_y))

    def detect_click(self, hand):
        clickdistance = utils.find_distance(hand, 4, 20)

        if clickdistance < 0.07:
            if not self.pinch_down:
                pyautogui.click()
                self.pinch_down = True
                print("Touching")

            else:
                self.pinch_down = False

    def detect_scroll(self, hand):
        scrolldistance = utils.find_distance(hand, 12, 4)

        if scrolldistance < 0.08:
            if not self.scrollmode:
                pyautogui.scroll(-50)
                print("Scroll")
                self.scrollmode = True

        else:
            self.scrollmode = False

    
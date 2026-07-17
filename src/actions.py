import mediapipe as mp
import pyautogui
import utils as utils


class ActionDetector:
    def __init__(self):
        self.pinch_down = False
        self.scroll_mode_down = False
        self.scroll_mode_up = False
        self.prev_pos_x, self.prev_pos_y = 400, 400
        self.screen_x, self.screen_y = pyautogui.size()

    def move(self, hand):
        pointer_x = hand.landmark[8].x

        pointer_x = (1-pointer_x) * self.screen_x
        pointer_y = (hand.landmark[8].y) * self.screen_y

        mouse_pos_x = (self.prev_pos_x + pointer_x)/2 #Find average to smooth jittering
        mouse_pos_y = (self.prev_pos_y + pointer_y)/2

        pyautogui.moveTo(int(mouse_pos_x), int(mouse_pos_y))

        self.prev_pos_x = mouse_pos_x
        self.prev_pos_y = mouse_pos_y

    def detect_click(self, hand): #Detect click with pinky finger and thumb
        clickdistance = utils.find_distance(hand, 4, 20)

        if clickdistance < 0.07:
            if not self.pinch_down:
                pyautogui.click()
                self.pinch_down = True #Uses states to stop spamming
                print("Touching")

            else:
                self.pinch_down = False

    def detect_scroll(self, hand):
        scroll_down_distance = utils.find_distance(hand, 12, 4)
        scroll_up_distance = utils.find_distance(hand, 16, 4)

        #Scroll Down
        if scroll_down_distance < 0.08:
            if not self.scroll_mode_down:
                pyautogui.scroll(-50)
                print("Scroll Down")
                self.scroll_mode_down = True

        else:
            self.scroll_mode_down = False

        #Scroll Up
        if scroll_up_distance < 0.08:
            if not self.scroll_mode_up:
                pyautogui.scroll(50)
                print("Scroll Up")
                self.scroll_mode_up = True

        else:
            self.scroll_mode_up = False

    
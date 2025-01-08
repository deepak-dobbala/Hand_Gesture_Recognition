import pyautogui

class MouseController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        pyautogui.FAILSAFE = False

    def move(self, x, y):
        # Convert the coordinates to screen coordinates
        screen_x = int(x * self.screen_width)
        screen_y = int(y * self.screen_height)
        pyautogui.moveTo(screen_x, screen_y)

    def click(self):
        pyautogui.click()

    def double_click(self):
        pyautogui.doubleClick()

    def right_click(self):
        pyautogui.rightClick()

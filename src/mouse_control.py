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

    def zoom(self, factor):
        # Positive factor = zoom in, negative factor = zoom out
        if abs(factor) > 0.2:  # Increased threshold for more intentional zooming
            # Convert factor to scroll units (negative because scroll direction is inverted)
            scroll_amount = int(-factor * 10)  # Increased multiplier for more noticeable zoom
            
            # Limit the maximum scroll amount
            scroll_amount = max(min(scroll_amount, 5), -5)
            
            # Apply the zoom
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(scroll_amount)
            pyautogui.keyUp('ctrl')
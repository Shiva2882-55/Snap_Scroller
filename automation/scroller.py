import pyautogui
import time


class Scroller:
    """
    Handles OS-level scrolling actions.
    """

    def __init__(self, scroll_amount=-500):
        """
        scroll_amount:
        negative → scroll down
        positive → scroll up
        """
        self.scroll_amount = scroll_amount

    def scroll(self):
        pyautogui.scroll(self.scroll_amount)
        time.sleep(0.05)  # small delay for stability

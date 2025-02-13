import pyautogui
import time
import os
import yaml
import subprocess
import numpy as np

class Clicker:
    def __init__(self, loading_sleep_time=5, move_duration=1):
        pyautogui.PAUSE = 1
        self.loading_sleep_time = loading_sleep_time
        self.move_duration = move_duration
        self.available_programs = {"chrome": "Google Chrome", "vscode": "Visual Studio Code"}
        self.global_x, self.global_y = pyautogui.size()
        self.data = self.load_data()
        self.available_data = self.data.keys()

    def load_data(self, yaml_path="credentials.yaml"):
        with open(yaml_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def focus_program(self, program_name):
        if program_name not in self.available_programs:
            raise ValueError(f"Program {program_name} is not available.")
        selected_program = self.available_programs[program_name]

        applescript = f'tell application "{selected_program}" to activate'
        subprocess.run(["osascript", "-e", applescript])
        time.sleep(self.move_duration)

    def find(self, image_path):
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Image {image_path} not found.")

        try:
            button_location = pyautogui.locateOnScreen(image_path, confidence=0.9)
        except:
            raise ValueError(f"Image {image_path} not found on screen.")

        button_center = pyautogui.center(button_location)
        img_x, img_y = int(button_center[0]*0.5), int(button_center[1]*0.5)
        return img_x, img_y
    
    def check_image_on_screen(self, check_img, num_retries=4):
        for i in range(num_retries):
            try:
                self.find(check_img)
                return True
            except:
                if i == num_retries-1:
                    return False
                pyautogui.hotkey('command', 'r')
                time.sleep(self.loading_sleep_time)

    def click(self, x, y):
        self._validate_coordinates(x, y)
        pyautogui.click(x=x, y=y)

    def move(self, x, y):
        self._validate_coordinates(x, y)
        pyautogui.moveTo(x, y, self.move_duration, pyautogui.easeOutQuad)

    def scroll_down(self, amount):
        if not isinstance(amount, int):
            raise ValueError("Scroll amount must be an integer.")
        pyautogui.scroll(-amount)

    def find_move(self, image_path):
        img_x, img_y = self.find(image_path)
        self.move(img_x, img_y)
        return img_x, img_y

    def find_move_click(self, image_path):
        img_x, img_y = self.find_move(image_path)
        self.click(img_x, img_y)

    def find_move_click_write(self, image_path, info_key):
        if info_key not in self.available_data:
            raise ValueError(f"{info_key} is not loaded in data.")
        self.find_move_click(image_path)
        pyautogui.write(self.data[info_key])

    def _validate_coordinates(self, x, y):
        if not isinstance(x, (int, float, np.int64)) or not isinstance(y, (int, float, np.int64)):
            raise ValueError("Coordinates must be numeric.")

    def open_browser(self):
        applescript = """
        do shell script "open -n -a 'Google Chrome'"
        """
        subprocess.run(["osascript", "-e", applescript])
        time.sleep(3)
        self.find_move_click('find_img/google_profile.png')
        time.sleep(3)

    def open_website(self, website):
        pyautogui.hotkey('command', 'l')
        pyautogui.write(website)
        pyautogui.hotkey('enter')
        time.sleep(3)


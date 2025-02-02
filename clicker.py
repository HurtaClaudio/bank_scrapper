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
            print(button_location)
        except:
            raise ValueError(f"Image {image_path} not found on screen.")

        button_center = pyautogui.center(button_location)
        img_x, img_y = int(button_center[0]*0.5), int(button_center[1]*0.5)
        return img_x, img_y
    
    def check_image_on_screen(self, check_img):
        try:
            for i in range(4):
                try:
                    self.find(check_img)
                    break
                except:
                    if i == 3:
                        raise ValueError(f'img "{check_img}" not found.')
                    pyautogui.hotkey('command', 'r')
                    time.sleep(self.loading_sleep_time)
        except:
            ValueError(f"Program failed to find {check_img}, unstable UI.")


    def click(self, x, y):
        if not isinstance(x, (int, float, np.int64)) or not isinstance(y, (int, float, np.int64)):
            raise ValueError("Coordinates must be numeric.")

        pyautogui.click(x=x, y=y)

    def move(self, x, y):
        if not isinstance(x, (int, float, np.int64)) or not isinstance(y, (int, float, np.int64)):
            raise ValueError("Coordinates must be numeric.")

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


if __name__ == "__main__":
    clicker = Clicker()
    clicker.open_browser()
    clicker.open_website('bice.cl')

    clicker.find_move_click('find_img/ingresar.png')
    clicker.find_move_click('find_img/personas.png')
    time.sleep(clicker.loading_sleep_time)

    clicker.find_move_click_write(image_path='find_img/rut.png', info_key='rut')
    clicker.find_move_click_write(image_path='find_img/clave.png', info_key='bice_pass')
    clicker.find_move_click('find_img/ingresar_2.png')
    time.sleep(clicker.loading_sleep_time)

    clicker.find_move_click('find_img/cuentas.png')
    clicker.find_move_click('find_img/cuenta_corriente.png')
    clicker.find_move_click('find_img/saldos_movimientos.png')
    time.sleep(clicker.loading_sleep_time)

    clicker.check_image_on_screen('find_img/check_saldos_movimientos.png')
    clicker.scroll_down(10)
    clicker.find_move_click('find_img/descargar.png')
    time.sleep(clicker.loading_sleep_time)

    clicker.focus_program(program_name='vscode')
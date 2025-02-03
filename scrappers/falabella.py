import sys
import os
import time
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Clicker import Clicker
from DataHandler import DataHandler
from DBHandler import DBHandler

def setup_falabella_landing_page(clicker):
    clicker.open_browser()
    clicker.open_website('bancofalabella.cl')

def navigate_landing(clicker):
    clicker.find_move_click('find_img/falabella/mi_cuenta.png')
    time.sleep(clicker.loading_sleep_time)

def navigate_authentication(clicker):
    clicker.find_move_click_write(image_path='find_img/falabella/rut.png', info_key='rut')
    clicker.find_move_click_write(image_path='find_img/falabella/pass.png', info_key='falabella_pass')
    clicker.find_move_click('find_img/falabella/ingresar.png')
    time.sleep(clicker.loading_sleep_time)
    time.sleep(5)

def navigate_to_tarjeta_credito(clicker):
    clicker.scroll_down(15)
    clicker.find_move_click('find_img/falabella/tarjeta_credito.png')
    time.sleep(clicker.loading_sleep_time)

def navigate_tarjeta_credito_download_movimientos(clicker):
    clicker.check_image_on_screen('find_img/falabella/check_tc.png')
    clicker.scroll_down(15)
    clicker.find_move_click('find_img/falabella/download_data.png')
    clicker.scroll_down(-15)
    time.sleep(clicker.loading_sleep_time)

def scrapper():
    clicker = Clicker()
    setup_falabella_landing_page(clicker)

    if clicker.check_image_on_screen('find_img/falabella/check_landing.png', num_retries=1):
        navigate_landing(clicker)

    navigate_authentication(clicker)
    navigate_to_tarjeta_credito(clicker)
    navigate_tarjeta_credito_download_movimientos(clicker)

    clicker.focus_program(program_name='vscode')

def proces_files():
    data_handler = DataHandler()
    data_handler.process_latest_file(data_handler.pattern_tc_falabella)
    data_handler.delete_old_files(data_handler.pattern_tc_falabella) 

def add_to_db():
    db_handler = DBHandler()

    df_tc = pd.read_csv("results/results_tc_falabella.csv")
    db_handler.save_to_db(df_tc)
    db_handler.query_db()

    db_handler.close_connection()

def test():
    pass

if __name__ == "__main__":
    scrapper()
    proces_files()
    add_to_db()
    #test()
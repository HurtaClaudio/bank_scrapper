import sys
import os
import time
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Clicker import Clicker
from DataHandler import DataHandler
from DBHandler import DBHandler

def setup_bice_landing_page(clicker):
    clicker.open_browser()
    clicker.open_website('bice.cl')

def navigate_home(clicker):
    clicker.find_move_click('find_img/ingresar.png')
    clicker.find_move_click('find_img/personas.png')
    time.sleep(clicker.loading_sleep_time)

def navigate_authentication(clicker):
    clicker.find_move_click_write(image_path='find_img/rut.png', info_key='rut')
    clicker.find_move_click_write(image_path='find_img/clave.png', info_key='bice_pass')
    clicker.find_move_click('find_img/ingresar_2.png')
    time.sleep(clicker.loading_sleep_time)
    time.sleep(5)

def navigate_to_cuenta_corriente(clicker):
    clicker.find_move_click('find_img/cuentas.png')
    clicker.find_move_click('find_img/cuenta_corriente.png')
    clicker.find_move_click('find_img/saldos_movimientos.png')
    time.sleep(clicker.loading_sleep_time)

def navigate_cuenta_corriente_download_movimientos(clicker):
    clicker.check_image_on_screen('find_img/check_saldos_movimientos.png')
    clicker.scroll_down(10)
    clicker.find_move_click('find_img/descargar.png')
    clicker.scroll_down(-10)
    time.sleep(clicker.loading_sleep_time)

def navigate_to_tarjeta_credito(clicker):
    clicker.find_move_click('find_img/tarjeta_credito.png')
    clicker.find_move_click('find_img/consultas.png')
    clicker.find_move_click('find_img/consultas_tc.png')
    time.sleep(clicker.loading_sleep_time)

def navigate_tarjeta_credito_download_movimientos(clicker):
    clicker.check_image_on_screen('find_img/check_tc.png')
    clicker.scroll_down(15)
    clicker.find_move_click('find_img/descargar.png')
    clicker.scroll_down(-15)
    time.sleep(clicker.loading_sleep_time)

def scrapper():
    clicker = Clicker()
    setup_bice_landing_page(clicker)

    navigate_home(clicker)

    if clicker.check_image_on_screen('find_img/check_auth.png', num_retries=1):
        navigate_authentication(clicker)

    navigate_to_cuenta_corriente(clicker)    
    navigate_cuenta_corriente_download_movimientos(clicker)

    navigate_to_tarjeta_credito(clicker)
    navigate_tarjeta_credito_download_movimientos(clicker)

    clicker.focus_program(program_name='vscode')

def proces_files():
    data_handler = DataHandler()
    data_handler.process_latest_file(data_handler.pattern_cuenta_corriente)
    data_handler.delete_old_files(data_handler.pattern_cuenta_corriente)

    data_handler.process_latest_file(data_handler.pattern_tarjeta_credito)
    data_handler.delete_old_files(data_handler.pattern_tarjeta_credito)

def add_to_db():
    db_handler = DBHandler()

    df_cc = pd.read_csv("results_cc.csv")
    df_tc = pd.read_csv("results_tc.csv")

    db_handler.save_to_db(df_cc)
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
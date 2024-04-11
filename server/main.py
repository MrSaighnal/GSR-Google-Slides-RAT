import time
import threading
from google.oauth2 import service_account
from googleapiclient.discovery import build
import base64
from colorama import Fore, Back, Style
from modules.config import service_account_info, presentation_id, SCOPES, sleep_time
from modules.utils import get_current_date_time, generate_hash_md5, execute_command, print_terminal_start, print_banner, print_configuration
from modules.google_services import insert_text_into_cell, replace_text_in_cell, find_empty_raw_in_table
from modules.background_tasks import background_task
from modules.extend_command import check_command
from modules.help import print_help


def main():
    credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    # background thread
    background_thread = threading.Thread(target=background_task, args=(credentials, presentation_id), daemon=True)
    background_thread.start()

    # input management
    try:
        print_terminal_start()
        while True:
            
            command = input().strip().lower()
            if command == "exit":
                print("quitting...")
                break
            elif command == "help":
                print_help()
                print_terminal_start()
            else:
                if not check_command(command):
                    service = build('slides', 'v1', credentials=credentials)
                    presentation = service.presentations().get(presentationId=presentation_id).execute()
                    for slide in presentation.get('slides', []):
                        for elem in slide.get('pageElements', []):
                            if 'table' in elem:
                                table_id = elem['objectId']
                    row_index = find_empty_raw_in_table(service, presentation_id, table_id)
                    insert_text_into_cell(service, presentation_id, table_id, row_index, 1, command)
    except KeyboardInterrupt:
        print("\nquitting...")

if __name__ == "__main__":
    print_banner()
    print_configuration()
    main()
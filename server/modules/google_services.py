def find_empty_raw_in_table(service, presentation_id, table_id):
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    
    for slide in presentation.get('slides', []):
        for elem in slide.get('pageElements', []):
            if elem.get('objectId') == table_id and 'table' in elem:
                table = elem['table']
                for row_index, row in enumerate(table.get('tableRows', [])):
                    tutte_colonne_vuote = True  
                    
                    for cell in row.get('tableCells', []):
                        text_elements = cell.get('text', {}).get('textElements', [])
                        cell_text = ''.join([text_element.get('textRun', {}).get('content', '').strip() for text_element in text_elements])
                        
                        if cell_text:
                            tutte_colonne_vuote = False
                            break
                    
                    if tutte_colonne_vuote:
                        return row_index




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

def replace_text_in_cell(service, presentation_id, table_id, row_index, column_index, new_text):
    requests = [
        {
            'deleteText': {
                'objectId': table_id,
                'cellLocation': {
                    'rowIndex': row_index,
                    'columnIndex': column_index,
                },
                'textRange': {
                    'type': 'ALL'
                }
            }
        },
        {
            'insertText': {
                'objectId': table_id,
                'cellLocation': {
                    'rowIndex': row_index,
                'columnIndex': column_index,
                },
                'text': new_text,
                'insertionIndex': 0,
            }
        }
    ]

    body = {'requests': requests}
    response = service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()

import time
from datetime import datetime
from pytz import timezone
import constants
from google_service import google_service
from spreadsheets import Sheet
from database import DatabaseConnector
from drive_permission import give_edit_access, move_files_for_james
from client_article import ClientArticle


def main(data, context):
    time1 = time.time()

    editor_sheets_service = google_service(constants.SHEETS)
    content_flow = Sheet(editor_sheets_service, constants.CLIENT_SPREADSHEET)
    database_connection = DatabaseConnector()

    values = database_connection.get_spreadsheet_cards()
    doc_files = []
    sheets = []

    for value in values:
        doc_link = value[4]
        # Only select the Google Doc links from FinalDocLinks
        if doc_link.startswith('https://docs.google.com/document/d/'):
            doc_files.append(value[4])
        sheets.append(value[10])

    give_edit_access(doc_files)

    # Instantiating ClientArticle objects
    ClientArticle.instantiate_from_db_list(values)

    dict_sheet = {}
    sheets = set(sheets)

    # Aggregating articles for each sheet
    for sheet in sheets:
        dict_sheet[sheet] = ClientArticle.return_articles_by_sheet(sheet)

    for key in dict_sheet.keys():
        spreadsheet_range = key + constants.SHEET_DEFAULT_RANGE
        values = dict_sheet[key]
        print(values)
        content_flow.append_values(spreadsheet_range, values)

    james_articles = ClientArticle.return_james_articles()
    move_files_for_james(james_articles)

    database_connection.update_status_ready(ClientArticle.update_article_status())

    client_sheets = database_connection.get_client_sheets()
    sent_values = []
    uploaded_values = []

    for sheet in client_sheets:
        rn = content_flow.get_values(f'{sheet[0]}!K1')[0][0]
        vals = content_flow.get_values(f'{sheet[0]}!{rn}')

        now = datetime.now(timezone('Asia/Kolkata'))
        now = now.strftime('%Y-%m-%d %H:%M:%S')

        for val in vals:
            if val[-1] == 'Submitted':
                sent_values.append([constants.STATUS_SUBMITTED, now, val[0]])
            elif val[-1] == 'Uploaded':
                uploaded_values.append([constants.STATUS_UPLOADED, now, val[0]])

    database_connection.update_status_sent(sent_values)
    database_connection.update_status_uploaded(uploaded_values)

    database_connection.connection.close()

    time2 = time.time()

    print(f'Time taken: {time2 - time1} seconds')


if __name__ == '__main__':
    main('', '')

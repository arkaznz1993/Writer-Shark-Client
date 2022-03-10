import os
import mysql.connector
from mysql.connector.constants import ClientFlag

# Instance name - flash-hour-338103:asia-south1:test-sql-server
# Service Account Email - flash-hour-338103@appspot.gserviceaccount.com

config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': '35.200.140.194',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': os.environ.get('SSL_CA'),
    'ssl_cert': os.environ.get('SSL_CERT'),
    'ssl_key': os.environ.get('SSL_KEY'),
    'database': os.environ.get('DB_NAME'),
}

GET_SPREADSHEET_CARDS = 'SELECT CardDetails.CardId, CardDetails.CardTitle, CardDetails.CardUrl, ' \
                        'CardDetails.SurferSEOLink, CardDetails.FinalDocLink,' \
                        'CardDetails.WordCount, Writers.Name, CardDetails.CompletedDate, ' \
                        'Clients.Name AS Client, Clients.Sheet ' \
                        'FROM CardDetails JOIN Writers ON CardDetails.Writer = Writers.TrelloId ' \
                        'JOIN Clients ON CardDetails.Client = Clients.Id ' \
                        'WHERE CardDetails.Status = 2 ' \
                        'ORDER BY CardDetails.CompletedDate ASC;'

GET_SHEETS = "SELECT DISTINCT Sheet FROM Clients WHERE Sheet != '';"

UPDATE_STATUS_SPREADSHEET = 'UPDATE CardDetails SET Status = %s WHERE CardId = %s'


class DatabaseConnector:
    def __init__(self):
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()

    def get_spreadsheet_cards(self):
        self.cursor.execute(GET_SPREADSHEET_CARDS)
        return self.cursor.fetchall()

    def get_client_sheets(self):
        self.cursor.execute(GET_SHEETS)
        return self.cursor.fetchall()

    def update_status(self, values):
        self.cursor.executemany(UPDATE_STATUS_SPREADSHEET, values)
        self.connection.commit()


database_connection = DatabaseConnector()
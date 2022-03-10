import os

GOOGLE_DOC_LINK = 'https://docs.google.com/document/d/[DOC_ID]/edit'
USER_EMAIL = 'editor@writershark.com'

CLIENT_SPREADSHEET = '1JWpQxJfUsxafHRVacoz5dAPa7fQHcjuwThQYNifjb0c'
SHEET_DEFAULT_RANGE = '!A2:I'

# Service type constants for Google Services
SHEETS = 1
DOCS = 2
DRIVE = 3

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/gmail.send']

# Date Time Related Things
DATE_FORMAT = '%Y-%m-%d'


STATUS_SUBMITTED = 4
STATUS_UPLOADED = 5

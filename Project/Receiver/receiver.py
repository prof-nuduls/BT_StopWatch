#!/usr/bin/env python3
from __future__ import print_function
import serial
import time

# Open serial port at 115200 baud
ser = serial.Serial(port='/dev/ttyS5', baudrate=9600)


import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account
import time, sys

# Creating Google Sheets Scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

credentials = None
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '155wiO3Gij60yzbDigzpCZG1kRkzmlNSO7ySp7FKt0g4'
user = ['Tux!A2','Boris!A2']
SAMPLE_RANGE_NAME = 'Boris!A2'

while True:
    values = []
    while True:
        time.sleep(0.5)
        while(ser.inWaiting()!=0):
            values.append((ser.read(ser.inWaiting()).decode().split(',')))
            print(values)
            if values[0][0] == '1':
                SAMPLE_RANGE_NAME = user[1]
                values[0].remove('1')
            else:
                SAMPLE_RANGE_NAME = user[0]
                values[0].remove('2')

        if len(values) != 0:
            break   

    # Create service and call it 
    service = build('sheets', 'v4', credentials=credentials)
    # Call the Sheets API
    sheet = service.spreadsheets()
    body = {'values': values}
    result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME,
                                valueInputOption='USER_ENTERED', 
                                body=body
                                ).execute()

    print(result)
    for row in values:
        print(row)
ser.close()
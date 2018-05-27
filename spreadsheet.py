"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import config
import util
import math
import os

def main():
    # Setup the Sheets API
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    store = file.Storage(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'credentials.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'client_secret.json'), SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    result = service.spreadsheets().values().get(spreadsheetId=config.SPREADSHEET_ID,
                                                range=config.SPREADSHEET_DATA_RANGE).execute()
    values = result.get('values', [])
    
    auctions, timestamp = util.download_auctions_json()
    
    if (values[0][2] != timestamp):
        values_updated = update_prices(values, auctions)
        values_updated[0][2] = timestamp

        if values_updated is not None and len(values) == len(values_updated):
            body = {
                'values': values
            }

            result = service.spreadsheets().values().update(
                spreadsheetId=config.SPREADSHEET_ID, range=config.SPREADSHEET_DATA_RANGE,
                valueInputOption='USER_ENTERED', body=body).execute()

            print('{0} cells updated.'.format(result.get('updatedCells')))
        else:
            print("Error! Price update malfunction.")
    else:
        print("No updates.")

def update_prices(sheet_data, auctions):
    mins = {}

    for auction in auctions:
        item_id = auction['item']
        price = math.floor(auction['buyout'] / auction['quantity']) if auction['quantity'] > 1 else auction['buyout']

        # If we don't have a minimum already, or if it's a new minimum:
        if (item_id not in mins.keys() or mins[item_id] > price) and price > 0:
            mins[item_id] = price
        
    for row in sheet_data:
        try:
            if len(row) > 1:
                id = int(row[0])
                price = util.SplitGoldString(mins[id])
                row[2] = price[0]
                row[3] = price[1]
                row[4] = price[2]

        except ValueError as identifier:
            pass

    return sheet_data

if __name__ == "__main__":
    main()
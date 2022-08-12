import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from typing import List
from data_loader import Expense

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def create_authorized_service():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        # print("sheets service created successfully")
        return service
    except HttpError as err:
        print(err)


def create_sheet(service):
    sheet_body = {
        "properties": {
            "title": "Expenses",
            "locale": "en_US",
        },
    }

    sheets_file = service.spreadsheets().create(body=sheet_body).execute()
    print("\n\nCreated sheet:")
    print(sheets_file["spreadsheetUrl"])
    print(sheets_file['spreadsheetId'])



def update_values(service, spreadsheet_id, expenses: List[Expense]):
    cell_range_insert = "A1"
    values = [
        ["Item", "Category", "Amount", "Importance"],
    ]

    for e in expenses:
        values.append([e.item, e.category.value, e.price, e.importance.value])

    value_range_body = {"majorDimension": "ROWS", "values": values}

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        valueInputOption="USER_ENTERED",
        range=cell_range_insert,
        body=value_range_body,
    ).execute()


def format_cells(service, spreadsheet_id, sheetId=0):
    reqs = {
        "requests": [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheetId,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                    },
                    "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
                    "fields": "userEnteredFormat.textFormat.bold",
                }
            },
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheetId,
                        "startColumnIndex": 2,
                        "endColumnIndex": 3,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "numberFormat": {
                                "type": "CURRENCY",
                                "pattern": '"$"#,##0.00',
                            }
                        }
                    },
                    "fields": "userEnteredFormat.numberFormat",
                }
            },
        ]
    }

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body=reqs
    ).execute()


def create_pivot_table(service, spreadsheet_id, sheetId, data):
    request_body = {
        "requests": [
            {
                "updateCells": {
                    "rows": {
                        "values": [
                            {
                                "pivotTable": {
                                    "source": {
                                        "sheetId": sheetId,
                                        "startRowIndex": 0,
                                        "endRowIndex": len(data) + 1,
                                        "startColumnIndex": 0,
                                        "endColumnIndex": 4,
                                    },
                                    "rows": [
                                        {
                                            "sourceColumnOffset": 1,
                                            "showTotals": True,
                                            "sortOrder": "DESCENDING",
                                            "valueBucket": {},  # sort according to SUM of values
                                        }
                                    ],
                                    "values": [
                                        {
                                            "sourceColumnOffset": 2,
                                            "summarizeFunction": "SUM",
                                        }
                                    ],
                                    "valueLayout": "HORIZONTAL",
                                }
                            }
                        ]
                    },
                    "start": {
                        "sheetId": sheetId,
                        "rowIndex": 0,
                        "columnIndex": 5,
                    },
                    "fields": "pivotTable",
                }
            },
            {
                "updateCells": {
                    "rows": {
                        "values": [
                            {
                                "pivotTable": {
                                    "source": {
                                        "sheetId": sheetId,
                                        "startRowIndex": 0,
                                        "endRowIndex": len(data) + 1,
                                        "startColumnIndex": 0,
                                        "endColumnIndex": 4,
                                    },
                                    "rows": [
                                        {
                                            "sourceColumnOffset": 3,
                                            "showTotals": True,
                                            "sortOrder": "DESCENDING",
                                            "valueBucket": {},  # sort according to SUM of values
                                        }
                                    ],
                                    "values": [
                                        {
                                            "sourceColumnOffset": 2,
                                            "summarizeFunction": "SUM",
                                        }
                                    ],
                                    "valueLayout": "HORIZONTAL",
                                }
                            }
                        ]
                    },
                    "start": {
                        "sheetId": sheetId,
                        "rowIndex": 0,
                        "columnIndex": 8,
                    },
                    "fields": "pivotTable",
                }
            },
        ]
    }

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body=request_body
    ).execute()

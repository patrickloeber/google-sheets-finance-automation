# Sheets tutorial

## Prerequisites

- A file named `expenses.csv` in the same folder with the item name and the amount, separated by a comma.
- A file `credentials.json` in the same folder.

## 1. Setup Google Cloud Project

- Create a new project on [https://console.cloud.google.com/](https://console.cloud.google.com/). Don't forget to switch to this project afterwards
- Enable the Google Sheets API
- OAuth consent screen -> External -> Fill out required fields with an email, also add this email under Test users.
- Create credentials: Credentials -> OAuth 2.0 Client IDs -> Desktop App. Download the json file and save it as `credentials.json` file in the project folder.

## (2. Optional: Create a virtual environment)

```console
python3 -m venv venv
. venv/bin/activate
```

## 3. Install requirements

```console
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## 4. Authorize the app and create the sheet

Run

```console
python create_sheet.py
```

The first time you run this a browser will open and you have to login.

It creates and prints the sheetId. Copy this Id and put it in [update_sheets.py](update_sheets.py), line 9.

## 5. Update the sheets file

Run

```console
python update_sheets.py
```

## References

- [Python Quick Start](https://developers.google.com/sheets/api/quickstart/python)
- [Update Cells](https://developers.google.com/sheets/api/guides/values)
- [Cell Formatting](https://developers.google.com/sheets/api/guides/formats)
- [Pivot Tables](https://developers.google.com/sheets/api/guides/pivot-tables)

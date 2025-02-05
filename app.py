from flask import Flask, jsonify
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

app = Flask(__name__)

# Lấy API key từ biến môi trường trên Render
SERVICE_ACCOUNT_FILE = "service_account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = "1Xvu28-7Qa5tjVgOqS8EY72NvxD_vJLnXzDrDRGo4spA"
RANGE_NAME = "Cozy!A1:J80"

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build("sheets", "v4", credentials=creds)

@app.route("/")
def home():
    return "Flask API for Google Sheets is running!"

@app.route("/get_data", methods=["GET"])
def get_data():
    """Lấy dữ liệu từ Google Sheets"""
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get("values", [])

    if not values:
        return jsonify({"error": "Không có dữ liệu"}), 400

    return jsonify({"data": values})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

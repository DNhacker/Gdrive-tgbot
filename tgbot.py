import json
import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 🔹 Load Telegram Credentials from tg.json
with open("tg.json", "r") as file:
    config = json.load(file)

BOT_TOKEN = config["bot_token"]
ADMIN_ID = config["admin_id"]
ALLOWED_USERS = set(config["allowed_users"])  # Convert list to set for fast lookup

# 🔹 Load Google Drive API Credentials
GDRIVE_CREDENTIALS = "service_account.json"
creds = Credentials.from_service_account_file(GDRIVE_CREDENTIALS, scopes=["https://www.googleapis.com/auth/drive"])
drive_service = build("drive", "v3", credentials=creds)

# 🔹 Setup Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# 🔹 Save Updated User List to tg.json
def save_users():
    config["allowed_users"] = list(ALLOWED_USERS)  # Convert set back to list
    with open("tg.json", "w") as file:
        json.dump(config, file, indent=4)

# 🔹 Extract Google Drive File ID from URL
def extract_drive_id(url):
    if "drive.google.com" in url:
        if "id=" in url:
            return url.split("id=")[1].split("&")[0]
        elif "/d/" in url:
            return url.split("/d/")[1].split("/")[0]
    return None

# 🔹 Get Google Drive Direct Download Link
def get_drive_download_url(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# 🔹 Start Command
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_USERS:
        update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    update.message.reply_text("✅ Send me a Google Drive video link, and I'll forward the video to you!")

# 🔹 Handle Google Dr

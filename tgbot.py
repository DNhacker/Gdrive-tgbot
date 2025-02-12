import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 🔹 Replace with your Telegram Bot Token
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# 🔹 Google Drive API Credentials
GDRIVE_CREDENTIALS = "service_account.json"  # Path to your JSON key file

# 🔹 Authenticate Google Drive API
creds = Credentials.from_service_account_file(GDRIVE_CREDENTIALS, scopes=["https://www.googleapis.com/auth/drive"])
drive_service = build("drive", "v3", credentials=creds)

# 🔹 Setup Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# 🔹 Function to extract Google Drive file ID from a URL
def extract_drive_id(url):
    if "drive.google.com" in url:
        if "id=" in url:
            return url.split("id=")[1].split("&")[0]
        elif "/d/" in url:
            return url.split("/d/")[1].split("/")[0]
    return None

# 🔹 Function to Get Google Drive Direct Download Link
def get_drive_download_url(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# 🔹 Telegram Command: Start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a Google Drive video link, and I'll forward the video to you!")

# 🔹 Telegram Message Handler: Stream Video from Google Drive
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chat_id = update.message.chat_id

    # Extract File ID
    file_id = extract_drive_id(user_message)
    if not file_id:
        update.message.reply_text("Invalid Google Drive link! Please send a valid video link.")
        return

    # Get File Info
    file_info = drive_service.files().get(fileId=file_id).execute()
    file_name = file_info["name"]
    
    update.message.reply_text(f"Forwarding video: {file_name}...")

    # Get Direct Download URL
    direct_url = get_drive_download_url(file_id)

    # Send Video to User Directly
    context.bot.send_video(chat_id=chat_id, video=direct_url, caption=file_name)

# 🔹 Main Function to Run the Bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

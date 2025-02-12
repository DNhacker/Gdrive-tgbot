import json
import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Debugging - Print when the bot starts
print("🚀 Bot is starting...")

# 🔹 Load Telegram Credentials from tg.json
try:
    with open("tg.json", "r") as file:
        config = json.load(file)
except FileNotFoundError:
    print("❌ Error: tg.json file not found! Please create it and add your bot token and admin ID.")
    exit(1)

BOT_TOKEN = config.get("bot_token")
ADMIN_ID = config.get("admin_id")
ALLOWED_USERS = set(config.get("allowed_users", []))  # Convert list to set for fast lookup

if not BOT_TOKEN:
    print("❌ Error: Bot token is missing in tg.json!")
    exit(1)

if not ADMIN_ID:
    print("❌ Error: Admin ID is missing in tg.json!")
    exit(1)

# 🔹 Load Google Drive API Credentials
GDRIVE_CREDENTIALS = "service_account.json"
try:
    creds = Credentials.from_service_account_file(GDRIVE_CREDENTIALS, scopes=["https://www.googleapis.com/auth/drive"])
    drive_service = build("drive", "v3", credentials=creds)
except FileNotFoundError:
    print("❌ Error: service_account.json file not found! Please add your Google Drive API credentials.")
    exit(1)

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
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    await update.message.reply_text("✅ Send me a Google Drive video link, and I'll forward the video to you!")

# 🔹 Handle Google Drive Link
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return

    user_message = update.message.text
    chat_id = update.message.chat_id

    # Extract File ID
    file_id = extract_drive_id(user_message)
    if not file_id:
        await update.message.reply_text("❌ Invalid Google Drive link! Please send a valid video link.")
        return

    # Get File Info
    try:
        file_info = drive_service.files().get(fileId=file_id).execute()
        file_name = file_info["name"]
    except Exception as e:
        await update.message.reply_text("❌ Error retrieving file info from Google Drive.")
        print("Google Drive API Error:", e)
        return

    await update.message.reply_text(f"📥 Forwarding video: {file_name}...")

    # Get Direct Download URL
    direct_url = get_drive_download_url(file_id)

    # Send Video to User Directly
    try:
        await context.bot.send_video(chat_id=chat_id, video=direct_url, caption=file_name)
    except Exception as e:
        await update.message.reply_text("❌ Failed to send video. The file might be too large or restricted.")
        print("Telegram API Error:", e)

# 🔹 Add User Command (Admin Only)
async def add_user(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Only the admin can add users!")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /adduser <user_id>")
        return

    try:
        new_user = int(context.args[0])
        if new_user in ALLOWED_USERS:
            await update.message.reply_text("⚠️ User is already authorized.")
        else:
            ALLOWED_USERS.add(new_user)
            save_users()
            await update.message.reply_text(f"✅ User {new_user} added successfully!")
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID. Please provide a numeric Telegram user ID.")

# 🔹 Remove User Command (Admin Only)
async def remove_user(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Only the admin can remove users!")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /removeuser <user_id>")
        return

    try:
        remove_user = int(context.args[0])
        if remove_user in ALLOWED_USERS:
            ALLOWED_USERS.remove(remove_user)
            save_users()
            await update.message.reply_text(f"✅ User {remove_user} removed successfully!")
        else:
            await update.message.reply_text("⚠️ User is not in the allowed list.")
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID. Please provide a numeric Telegram user ID.")

# 🔹 Show Allowed Users (Admin Only)
async def list_users(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Only the admin can view the user list!")
        return

    if not ALLOWED_USERS:
        await update.message.reply_text("⚠️ No users have been added yet.")
    else:
        user_list = "\n".join(map(str, ALLOWED_USERS))
        await update.message.reply_text(f"✅ Allowed Users:\n{user_list}")

# 🔹 Main Function to Run the Bot
def main():
    print("✅ Bot is now running...")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("adduser", add_user))
    app.add_handler(CommandHandler("removeuser", remove_user))
    app.add_handler(CommandHandler("listusers", list_users))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()

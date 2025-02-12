# Telegram Bot - Google Drive Video Downloader

This bot allows users to send a **Google Drive video link**, and it streams the video **directly** to the Telegram chat.

## 🚀 Features
- **No Local Storage**: Streams videos **directly** from Google Drive.
- **Fast & Secure**: Uses Telegram's built-in video player.
- **Simple Setup**: Just provide a Google Drive **service account key**.

---

## 📌 Setup Instructions

### 1️⃣ Install Required Dependencies
Run the following command to install necessary Python packages:
```bash
pip install python-telegram-bot google-auth google-auth-oauthlib google-auth-httplib2 googleapiclient requests
```

---

## 2️⃣ Enable Google Drive API & Get Service Account JSON

To allow the bot to access Google Drive, follow these steps:

### **🔹 Step 1: Enable Google Drive API**
1. **Go to Google Cloud Console**  
   👉 [https://console.cloud.google.com/](https://console.cloud.google.com/)  
2. **Select Your Project** or **Create a New Project**.  
3. In the left menu, go to **"APIs & Services" > "Library"**.  
4. Search for **"Google Drive API"** and click **Enable**.  

   📷 **Screenshot:** [View Here](https://i.imgur.com/4TfUibJ.png)  

---

### **🔹 Step 2: Create a Service Account**
1. **Go to IAM & Admin**:  
   👉 [https://console.cloud.google.com/iam-admin/serviceaccounts](https://console.cloud.google.com/iam-admin/serviceaccounts)  
2. Click **"Create Service Account"**.  
3. Fill in the details:  
   - **Service account name**: `gdrive-bot`  
   - **Service account ID**: (auto-generated)  
   - **Description**: `Service account for Telegram bot`  
4. Click **Create & Continue**.  
5. **Grant permissions** → Choose **"Editor"** or **"Owner"** (to allow file access).  
6. Click **Done** (You don’t need to add any users).  

   📷 **Screenshot:** [View Here](https://i.imgur.com/3A3gHXx.png)  

---

### **🔹 Step 3: Download the JSON Key File**
1. After creating the service account, **click on its email** in the list.  
2. Go to the **"Keys"** tab.  
3. Click **"Add Key" > "Create new key"**.  
4. Choose **"JSON"** format.  
5. Click **Create** → The file will **download automatically** (`service_account.json`).  
6. **Move this file to your bot’s project folder.**  

   📷 **Screenshot:** [View Here](https://i.imgur.com/VReLO9F.png)  

---

### **🔹 Step 4: Share Google Drive Files with the Service Account**
1. Open your **Google Drive**.  
2. Find the **video file or folder** you want to access.  
3. Right-click → **Share** → Add the **service account email** (found in `service_account.json`).  
4. Set **permission to "Viewer"**.  
5. Click **Done**.  

   📷 **Screenshot:** [View Here](https://i.imgur.com/GXkW8KY.png)  

---

## 3️⃣ Set Up the Telegram Bot
1. Go to **[@BotFather](https://t.me/BotFather)** on Telegram.  
2. Create a new bot using `/newbot` and get your **BOT_TOKEN**.  
3. Replace `"YOUR_TELEGRAM_BOT_TOKEN"` in the in tg.json.
4. Replace `"user_id"` with your id in tg.json

---

## 4️⃣ Run the Bot
Start the bot by running:
```bash
python bot.py
```

---

## 🎯 Usage
1. Send a **Google Drive video link** to the bot.
2. The bot will **extract the file ID** and stream the video directly to your chat.

---

## 📌 Notes
- The bot **only supports public/shared files**.
- For **private files**, the service account **must have access**.
- Ensure your **Google Drive quota** allows file access.

---

## ⚡ Troubleshooting
❌ **Error: Invalid Google Drive Link?**  
✔ Make sure the link follows this format:  
   ```
   https://drive.google.com/file/d/FILE_ID/view?usp=sharing
   ```

❌ **Bot Not Responding?**  
✔ Check if your bot is running and your Telegram bot token is correct.

❌ **Video Not Loading?**  
✔ Ensure the **service account** has permission to access the file.

---

## 📜 License
This project is open-source and can be modified freely.

---

**Made with ❤️ by [d8.pawan](https://www.instagram.com/d8.pawan)**

import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# ID của ứng dụng trên Google Play
APP_ID = "com.ducminh.tripple.match.finding"

app = Flask(__name__)

async def check_app_status():
    """Kiểm tra trạng thái của ứng dụng trên Google Play."""
    url = f"https://play.google.com/store/apps/details?id={APP_ID}"
    response = requests.get(url)
    if response.status_code == 200:
        return f"✅ Ứng dụng vẫn còn tồn tại trên Google Play."
    else:
        return f"❌ Ứng dụng đã bị gỡ hoặc không tồn tại."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gửi tin nhắn chào mừng."""
    await update.message.reply_text("Chào bạn! Tôi sẽ tự động kiểm tra trạng thái ứng dụng trên Google Play.")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kiểm tra trạng thái ứng dụng bằng ID mặc định."""
    status = await check_app_status()  # Gọi hàm kiểm tra với APP_ID mặc định
    await update.message.reply_text(status)

# Định nghĩa route để nhận các cập nhật từ Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, application.bot)
    application.update_queue.put(update)
    return 'OK', 200

def main():
    # Thay TOKEN bằng API Token của bot từ BotFather
    TOKEN = "7776250755:AAHpBGunt0Mz1o7RwnJtdCw5sXtakp8l9xw"

    # Tạo Application
    global application
    application = Application.builder().token(TOKEN).build()

    # Đăng ký lệnh
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check", check))

    # Cấu hình webhook
    webhook_url = "https://testbottelegram.onrender.com"  # Thay bằng URL của bạn trên Render
    application.bot.set_webhook(webhook_url)

    # Lắng nghe trên cổng đúng
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
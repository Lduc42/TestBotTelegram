from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import http.server
import socketserver
import threading

# ID của ứng dụng trên Google Play
APP_ID = "com.ducminh.tripple.match.finding"

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

def run_dummy_server():
    """Chạy HTTP server giả để mở cổng cho Render."""
    PORT = 5000  # Cổng mà Render yêu cầu mở (mặc định là 5000)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving dummy server on port {PORT}")
        httpd.serve_forever()

def main():
    # Thay TOKEN bằng API Token của bot từ BotFather
    TOKEN = "7776250755:AAHpBGunt0Mz1o7RwnJtdCw5sXtakp8l9xw"

    # Tạo Application
    application = Application.builder().token(TOKEN).build()

    # Đăng ký lệnh
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check", check))  # Tự động kiểm tra trạng thái

    # Tạo thread để chạy HTTP server giả
    threading.Thread(target=run_dummy_server, daemon=True).start()

    # Chạy bot
    application.run_polling()

if __name__ == "__main__":
    main()
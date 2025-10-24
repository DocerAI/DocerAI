import os
import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройки из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY')

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой бот 🤖\n"
        "Просто напиши мне что-нибудь, и я отвечу!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📝 **Доступные команды:**
/start - Начать работу
/help - Показать справку

💬 Просто напиши сообщение - я отвечу!
    """
    await update.message.reply_text(help_text)

def query_api(user_message: str) -> str:
    """Функция для запроса к API"""
    try:
        # ЗАМЕНИ НА СВОЙ API URL
        api_url = "https://api.example.com/chat"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "message": user_message,
            "api_key": API_KEY
        }
        
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json().get("response", "✅ Получил ответ от API!")
        else:
            return f"❌ Ошибка API: {response.status_code}"
            
    except Exception as e:
        return f"🤖 Бот работает! (Ошибка API: {str(e)})"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")
    
    api_response = query_api(user_message)
    await update.message.reply_text(api_response)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Ошибка: {context.error}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    print("🤖 Бот запущен на Render!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
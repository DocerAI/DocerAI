import os
import requests
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Настройки из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY')

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start_command(update: Update, context: CallbackContext):
    """Обработчик команды /start"""
    update.message.reply_text(
        "Привет! Я твой бот 🤖\n"
        "Просто напиши мне что-нибудь, и я отвечу!"
    )

def help_command(update: Update, context: CallbackContext):
    """Обработчик команды /help"""
    help_text = """
📝 **Доступные команды:**
/start - Начать работу
/help - Показать справку

💬 Просто напиши сообщение - я отвечу!
    """
    update.message.reply_text(help_text)

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

def handle_message(update: Update, context: CallbackContext):
    """Обработчик текстовых сообщений"""
    user_message = update.message.text
    
    # Показываем что бот печатает
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Получаем ответ от API
    api_response = query_api(user_message)
    
    # Отправляем ответ пользователю
    update.message.reply_text(api_response)

def error_handler(update: Update, context: CallbackContext):
    """Обработчик ошибок"""
    logger.error(f"Ошибка при обработке сообщения: {context.error}")

def main():
    """Основная функция"""
    # Создаем updater
    updater = Updater(token=BOT_TOKEN, use_context=True)
    
    # Получаем dispatcher
    dp = updater.dispatcher
    
    # Добавляем обработчики
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Добавляем обработчик ошибок
    dp.add_error_handler(error_handler)
    
    # Запускаем бота
    print("🤖 Бот запущен на Render!")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

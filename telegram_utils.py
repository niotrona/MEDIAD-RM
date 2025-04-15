from telegram import Bot

def send_telegram_message(bot_token: str, chat_id: str, message: str) -> bool:
    try:
        bot = Bot(token=bot_token)
        bot.send_message(chat_id=chat_id, text=message)
        return True
    except Exception as e:
        print(f"Telegram 전송 오류: {e}")
        return False

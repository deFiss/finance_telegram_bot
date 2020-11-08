from finance_telegram_bot import bot
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    b = bot.Bot()
    b.start()
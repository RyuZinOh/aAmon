import os

from dotenv import load_dotenv

from bot import create_bot, register_events

load_dotenv()
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("set the TOKEN inside the .env")

bot = create_bot()
register_events(bot)
bot.run(token=TOKEN)

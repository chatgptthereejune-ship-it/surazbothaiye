"""
Telegram Message Forward Bot

What it does:
- Any user can send a message to your bot.
- The bot forwards the message to you with:
  Name, Username, User ID, and message text.

Setup:
1. Create a bot using @BotFather and copy your BOT_TOKEN.
2. Install aiogram:
   pip install aiogram
3. IMPORTANT: Start your own bot once from your Telegram account.
4. Get your Telegram numeric user ID using @userinfobot or @RawDataBot.
5. Replace BOT_TOKEN and ADMIN_CHAT_ID below.
6. Run:
   python message_to_admin_bot.py

Note:
Telegram bots usually cannot message an admin by @username directly.
Use your numeric ADMIN_CHAT_ID for reliable delivery.
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

# ====== EDIT THESE ======
BOT_TOKEN = "8936363904:AAEDmjhZ-ZFy2NMIDd2arLSRiuoQF-wUNjI"
ADMIN_USERNAME = "@srz_heree"  # only shown in logs/help; numeric ID is required for sending
ADMIN_CHAT_ID = 123456789       # replace with your real Telegram numeric user ID
# ========================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def user_details(message: Message) -> str:
    user = message.from_user
    full_name = user.full_name if user else "Unknown"
    username = f"@{user.username}" if user and user.username else "No username"
    user_id = user.id if user else "Unknown"

    return (
        "📩 New Message Received\n\n"
        f"👤 Name: {full_name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 User ID: {user_id}\n"
    )


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Hi! Send me any message and I will forward it to the owner."
    )


@dp.message(F.text)
async def forward_text(message: Message):
    report = user_details(message)
    report += f"\n💬 Message:\n{message.text}"

    try:
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=report)
        await message.answer("✅ Your message has been sent.")
    except Exception as e:
        logging.exception("Failed to send message to admin")
        await message.answer("❌ Message could not be sent. Owner needs to set ADMIN_CHAT_ID correctly.")


@dp.message()
async def forward_other(message: Message):
    report = user_details(message)
    report += "\n📎 Message type: Non-text message"

    try:
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=report)
        await message.forward(chat_id=ADMIN_CHAT_ID)
        await message.answer("✅ Your message has been sent.")
    except Exception:
        logging.exception("Failed to send non-text message to admin")
        await message.answer("❌ Message could not be sent. Owner needs to set ADMIN_CHAT_ID correctly.")


async def main():
    print("Bot started...")
    print(f"Admin username: {ADMIN_USERNAME}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

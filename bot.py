import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import Config

bot = Client(
    "StringGenBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Start message
@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(
        "**Welcome to String Session Generator Bot!**\n\n"
        "Choose the type of session you want to generate:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎭 Pyrogram", callback_data="pyrogram")],
            [InlineKeyboardButton("⚡ Telethon", callback_data="telethon")]
        ])
    )

# Callback for choice
@bot.on_callback_query()
async def callback_handler(client, query):
    if query.data == "pyrogram":
        await query.message.reply_text("Send your **API_ID API_HASH** separated by space (or use defaults). Example:\n`12345 abcdefghijklmnop`")
        bot.set_attr("mode", "pyrogram")
    elif query.data == "telethon":
        await query.message.reply_text("Send your **API_ID API_HASH** separated by space (or use defaults). Example:\n`12345 abcdefghijklmnop`")
        bot.set_attr("mode", "telethon")

# Handle credentials and login
@bot.on_message(filters.text & filters.private)
async def generate_string(client, message):
    mode = getattr(bot, "mode", None)
    if not mode:
        return

    try:
        creds = message.text.split()
        api_id = int(creds[0]) if len(creds) > 0 else Config.API_ID
        api_hash = creds[1] if len(creds) > 1 else Config.API_HASH

        if mode == "pyrogram":
            async with Client("gen", api_id=api_id, api_hash=api_hash, in_memory=True) as app:
                string = await app.export_session_string()
                await message.reply_text(
                    f"✅ **Pyrogram String Session:**\n\n`{string}`\n\nKeep it safe!",
                    quote=True
                )

        elif mode == "telethon":
            client = TelegramClient(StringSession(), api_id, api_hash)
            await client.start()
            string = client.session.save()
            await client.disconnect()
            await message.reply_text(
                f"✅ **Telethon String Session:**\n\n`{string}`\n\nKeep it safe!",
                quote=True
            )

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
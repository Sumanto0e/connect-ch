from pyrogram import Client, filters

import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

app = Client("mybot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private)
async def reply_and_forward(client, message):
    await message.reply("Halo dari bot Pyrogram di Heroku!")
    await app.send_message(CHANNEL_ID, f"Pesan dari {message.from_user.first_name}: {message.text}")

app.run()

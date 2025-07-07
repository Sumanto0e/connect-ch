from pyrogram import Client, filters
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")  # bisa -100... atau @username

app = Client("mybot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private)
async def reply_and_forward(client, message):
    print(f"📥 Pesan masuk dari {message.from_user.first_name} ({message.from_user.id}): {message.text}")
    
    try:
        await message.reply("Halo dari bot Pyrogram di Heroku!")
        print("✅ Berhasil balas ke user.")
    except Exception as e:
        print(f"❌ Gagal balas ke user: {e}")
    
    try:
        await app.send_message(CHANNEL_ID, f"📢 Pesan dari {message.from_user.first_name}: {message.text}")
        print(f"✅ Berhasil kirim ke channel: {CHANNEL_ID}")
    except Exception as e:
        print(f"❌ Gagal kirim ke channel: {e}")

@app.on_message(filters.command("start"))
async def started(client, message):
    print("🚀 Bot menerima /start")
    await message.reply("Bot aktif!")

print("🚦 Bot sedang start...")
app.run()
print("🛑 Bot dimatikan.")

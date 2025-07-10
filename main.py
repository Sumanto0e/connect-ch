from pyrogram import Client, filters, idle
import os
import time
import datetime
import asyncio

# ⏱️ Sinkronisasi waktu dengan UTC (untuk menghindari error msg_id)
os.environ["TZ"] = "UTC"
time.tzset()
print(f"🕒 Timezone diset ke UTC: {datetime.datetime.utcnow()}")

# 🔐 Konfigurasi
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")  # Bisa @username atau -100...

app = Client("mybot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 📥 Balas pesan user dan forward ke channel
@app.on_message(filters.private)
async def reply_and_forward(client, message):
    print(f"📥 Pesan masuk dari {message.from_user.first_name} ({message.from_user.id}): {message.text}")

    try:
        await message.reply("Halo dari bot Pyrogram di Heroku!")
        print("✅ Berhasil balas ke user.")
    except Exception as e:
        print(f"❌ Gagal balas ke user: {e}")

    try:
        await client.send_message(CHANNEL_ID, f"📢 Pesan dari {message.from_user.first_name}: {message.text}")
        print(f"✅ Berhasil kirim ke channel: {CHANNEL_ID}")
    except Exception as e:
        print(f"❌ Gagal kirim ke channel: {e}")

# 🚀 Command /start
@app.on_message(filters.command("start"))
async def started(client, message):
    await message.reply("Bot aktif!")
    print("🚀 Bot menerima /start")

# 🧪 Command /test kirim ke channel
@app.on_message(filters.command("test"))
async def test_channel(client, message):
    print("🧪 Coba kirim ke channel...")
    try:
        await client.send_message(CH_

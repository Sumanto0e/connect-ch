from pyrogram import Client, filters
import os
import time
import datetime

# ⏱️ Sinkronisasi waktu (penting untuk Heroku)
os.environ["TZ"] = "UTC"
time.tzset()
print(f"🕒 Timezone diset ke UTC: {datetime.datetime.utcnow()}")

# 🔐 Konfigurasi dari ENV
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# 🔧 Inisialisasi Pyrogram Client
app = Client(
    "mybot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# 📥 Balas dan forward pesan pribadi
@app.on_message(filters.private)
async def reply_and_forward(client, message):
    print(f"📥 Dari {message.from_user.first_name} ({message.from_user.id}): {message.text}")

    try:
        await message.reply("Halo dari Pyrogram 1.4.6!")
        print("✅ Balas ke user.")
    except Exception as e:
        print(f"❌ Gagal balas: {e}")

    try:
        await client.send_message(CHANNEL_ID, f"📢 Dari {message.from_user.first_name}: {message.text}")
        print(f"✅ Kirim ke channel: {CHANNEL_ID}")
    except Exception as e:
        print(f"❌ Gagal kirim channel: {e}")

# 🚀 /start
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("✅ Bot aktif (v1.4.6)")
    print("🚀 /start dijalankan")

# 🧪 /test kirim ke channel
@app.on_message(filters.command("test"))
async def test(client, message):
    try:
        await client.send_message(CHANNEL_ID, "🔁 Tes dari /test.")
        await message.reply("✅ Tes berhasil.")
    except Exception as e:
        print(f"❌ Error kirim /test: {e}")
        await message.reply(f"❌ Error: {e}")

# 📡 /info
@app.on_message(filters.command("info"))
async def info(client, message):
    try:
        chat = await client.get_chat(CHANNEL_ID)
        member = await client.get_chat_member(CHANNEL_ID, "me")
        status = member.status if member else "Tidak ditemukan"
        await message.reply(
            f"📡 Channel: {chat.title}\n"
            f"ID: <code>{chat.id}</code>\n"
            f"Status bot: {status}"
        )
    except Exception as e:
        await message.reply(f"❌ Gagal ambil info: {e}")
        print(f"❌ Gagal info: {e}")

# 🏓 /ping
@app.on_message(filters.command("ping"))
async def ping(client, message):
    await message.reply("🏓 PONG!")

# 🔎 /peerid [username atau ID]
@app.on_message(filters.command("peerid"))
async def peerid(client, message):
    if len(message.command) < 2:
        await message.reply("⚠️ Contoh: <code>/peerid @namachannel</code>")
        return
    try:
        target = message.command[1]
        chat = await client.get_chat(target)
        await message.reply(
            f"👁️‍🗨️ Peer ID dari <b>{chat.title or chat.first_name}</b>:\n<code>{chat.id}</code>"
        )
        print(f"🔍 Peer ID dari {target}: {chat.id}")
    except Exception as e:
        await message.reply(f"❌ Gagal ambil peer ID: {e}")
        print(f"❌ Error peerid: {e}")

# 🟢 Jalankan bot
print("🚦 Bot sedang start...")
app.run()
print("🛑 Bot dimatikan.")

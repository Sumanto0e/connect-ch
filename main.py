from pyrogram import Client, Filters
import os
import time
import datetime

# ⏱️ Sinkronisasi waktu
os.environ["TZ"] = "UTC"
time.tzset()
print(f"🕒 Timezone diset ke UTC: {datetime.datetime.utcnow()}")

# 🔐 Konfigurasi
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")  # -100... atau @username

app = Client(
    session_name="mybot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# 📥 Pesan pribadi → balas dan forward
@app.on_message(Filters.private)
def reply_and_forward(client, message):
    print(f"📥 Dari {message.from_user.first_name} ({message.from_user.id}): {message.text}")

    try:
        message.reply("Halo dari Pyrogram 1.4.6!")
        print("✅ Balas ke user.")
    except Exception as e:
        print(f"❌ Gagal balas: {e}")

    try:
        client.send_message(CHANNEL_ID, f"📢 Dari {message.from_user.first_name}: {message.text}")
        print(f"✅ Kirim ke channel: {CHANNEL_ID}")
    except Exception as e:
        print(f"❌ Gagal kirim channel: {e}")

# 🚀 /start
@app.on_message(Filters.command("start"))
def start(client, message):
    message.reply("Bot aktif (v1.4.6)")
    print("🚀 Menerima /start")

# 🧪 /test
@app.on_message(Filters.command("test"))
def test(client, message):
    try:
        client.send_message(CHANNEL_ID, "🔁 Tes kirim dari /test.")
        message.reply("✅ Test berhasil.")
    except Exception as e:
        print(f"❌ Gagal test: {e}")
        message.reply(f"❌ Error: {e}")

# 📡 /info
@app.on_message(Filters.command("info"))
def info(client, message):
    try:
        chat = client.get_chat(CHANNEL_ID)
        member = client.get_chat_member(CHANNEL_ID, "me")
        status = member.status if member else "Tidak ditemukan"
        message.reply(
            f"📡 Channel: {chat.title}\n"
            f"ID: <code>{chat.id}</code>\n"
            f"Status bot: {status}"
        )
    except Exception as e:
        print(f"❌ Gagal info: {e}")
        message.reply(f"❌ Gagal ambil info: {e}")

# 🏓 /ping
@app.on_message(Filters.command("ping"))
def ping(client, message):
    message.reply("PONG!")

# 🔎 /peerid [username atau ID]
@app.on_message(Filters.command("peerid"))
def peerid(client, message):
    try:
        if len(message.command) < 2:
            message.reply("⚠️ Contoh: <code>/peerid @namachannel</code>")
            return

        target = message.command[1]
        chat = client.get_chat(target)
        message.reply(
            f"👁️‍🗨️ Peer ID dari <b>{chat.title or chat.first_name}</b>:\n"
            f"<code>{chat.id}</code>"
        )
        print(f"🔍 Peer ID dari {target}: {chat.id}")
    except Exception as e:
        print(f"❌ Gagal ambil peer ID: {e}")
        message.reply(f"❌ Gagal ambil peer ID: {e}")

# 🚦 Run bot
print("🚦 Bot sedang start...")
app.run()
print("🛑 Bot dimatikan.")

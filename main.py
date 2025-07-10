import os
import time
import datetime
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel
from telethon.errors import RPCError

# ⏱️ Sinkronisasi waktu
os.environ["TZ"] = "UTC"
time.tzset()
print(f"🕒 Timezone diset ke UTC: {datetime.datetime.utcnow()}")

# 🔐 Konfigurasi ENV
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")  # Format: -100xxxxxxxxxx

# 🔧 Inisialisasi Telethon Bot
client = TelegramClient('mybot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 🪪 Konversi channel ID ke PeerChannel
CHANNEL = PeerChannel(int(CHANNEL_ID.replace("-100", "")))

# 📥 Balas & forward pesan pribadi
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handler(event):
    user = await event.get_sender()
    msg = event.raw_text
    print(f"📥 Dari {user.first_name} ({user.id}): {msg}")

    try:
        await event.reply("Halo dari Telethon!")
        print("✅ Berhasil balas.")
    except Exception as e:
        print(f"❌ Gagal balas: {e}")

    try:
        await client.send_message(CHANNEL, f"📢 Dari {user.first_name}: {msg}")
        print(f"✅ Berhasil kirim ke channel {CHANNEL_ID}")
    except Exception as e:
        print(f"❌ Gagal kirim ke channel: {e}")

# 🚀 /start
@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("✅ Bot aktif (Telethon)")
    print("🚀 /start dijalankan")

# 🧪 /test
@client.on(events.NewMessage(pattern="/test"))
async def test(event):
    try:
        await client.send_message(CHANNEL, "🔁 Tes dari /test.")
        await event.reply("✅ Tes berhasil.")
    except Exception as e:
        await event.reply(f"❌ Gagal: {e}")
        print(f"❌ Error /test: {e}")

# 📡 /info
@client.on(events.NewMessage(pattern="/info"))
async def info(event):
    try:
        await event.reply(
            f"📡 Channel ID: <code>{CHANNEL_ID}</code>\n"
            f"PeerChannel ID: <code>{CHANNEL.channel_id}</code>"
        )
    except Exception as e:
        await event.reply(f"❌ Gagal ambil info: {e}")
        print(f"❌ Gagal info: {e}")

# 🏓 /ping
@client.on(events.NewMessage(pattern="/ping"))
async def ping(event):
    await event.reply("🏓 PONG!")

# 🔎 /peerid (tanpa get_entity)
@client.on(events.NewMessage(pattern=r"/peerid (.+)"))
async def peerid(event):
    input_id = event.pattern_match.group(1)
    try:
        peer_id = int(input_id)
        await event.reply(f"🔎 Peer ID:\n<code>{peer_id}</code>")
        print(f"✅ Peer ID diberikan: {peer_id}")
    except Exception as e:
        await event.reply(f"❌ Gagal parse peer ID: {e}")
        print(f"❌ Error peerid: {e}")

# ▶️ Start
print("🚦 Bot sedang start (Telethon)...")
client.run_until_disconnected()
print("🛑 Bot dimatikan.")

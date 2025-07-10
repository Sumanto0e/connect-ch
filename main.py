from pyrogram import Client, filters
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")  # bisa @username atau -100...

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

@app.on_message(filters.command("test"))
async def test_channel(client, message):
    print("🧪 Coba kirim ke channel...")
    try:
        await app.send_message(CHANNEL_ID, "🔁 Tes kirim channel dari /test.")
        await message.reply("✅ Kirim ke channel berhasil.")
    except Exception as e:
        print(f"❌ Test gagal: {e}")
        await message.reply(f"❌ Gagal kirim ke channel: {e}")

@app.on_message(filters.command("ping"))
async def ping(client, message):
    await message.reply("PONG!")

@app.on_message(filters.command("info"))
async def get_channel_info(client, message):
    try:
        chat = await client.get_chat(CHANNEL_ID)
        print(f"📡 Info channel: {chat.title} ({chat.id})")
        await message.reply(f"📡 Channel dikenali: {chat.title}\nID: `{chat.id}`")
    except Exception as e:
        print(f"❌ Gagal get_chat: {e}")
        await message.reply(f"❌ Gagal ambil info channel: {e}")

print("🚦 Bot sedang start...")
app.run()
print("🛑 Bot dimatikan.")

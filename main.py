from pyrogram import Client, filters, idle
import os
import time
import datetime
import asyncio

# Set timezone (tidak terlalu ngaruh kalau pakai fix yang ini)
os.environ["TZ"] = "UTC"
time.tzset()
print(f"🕒 Timezone diset ke UTC: {datetime.datetime.utcnow()}")

# Env config
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# FIX: Gunakan name=None untuk mode bot_token
app = Client(
    name=None,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir="."
)

@app.on_message(filters.private)
async def reply_and_forward(client, message):
    print(f"📥 Dari {message.from_user.first_name} ({message.from_user.id}): {message.text}")
    try:
        await message.reply("Halo dari bot Pyrogram!")
        await client.send_message(CHANNEL_ID, f"📢 Dari {message.from_user.first_name}: {message.text}")
        print("✅ Balas & kirim ke channel sukses.")
    except Exception as e:
        print(f"❌ Error: {e}")

@app.on_message(filters.command("start"))
async def started(client, message):
    await message.reply("Bot aktif!")

@app.on_message(filters.command("ping"))
async def ping(client, message):
    await message.reply("PONG!")

@app.on_message(filters.command("test"))
async def test_channel(client, message):
    try:
        await client.send_message(CHANNEL_ID, "🔁 Tes kirim ke channel.")
        await message.reply("✅ Berhasil kirim.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@app.on_message(filters.command("info"))
async def get_channel_info(client, message):
    try:
        chat = await client.get_chat(CHANNEL_ID)
        member = await client.get_chat_member(CHANNEL_ID, "me")
        await message.reply(
            f"📡 Channel: {chat.title}\nID: <code>{chat.id}</code>\nStatus bot: <b>{member.status}</b>"
        )
    except Exception as e:
        await message.reply(f"❌ Error ambil info: {e}")

async def main():
    print("🚦 Bot mulai...")
    await app.start()
    print("✅ Bot online.")
    await idle()
    await app.stop()
    print("🛑 Bot dimatikan.")

if __name__ == "__main__":
    asyncio.run(main())

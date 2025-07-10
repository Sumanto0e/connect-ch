from pyrogram import Client, filters
import os

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])  # -100xxxxxxxxxx
GRUB_ID = int(os.environ["GRUB_ID"])
DATABASE_ID = int(os.environ["DATABASE_ID"])

app = Client("mybot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("test"))
async def test(client, message):
    try:
        await client.send_message(CHANNEL_ID, "✅ Test dari Pyrogram bot.")
        await client.send_message(GRUB_ID, "✅ Test dari Pyrogram bot.")
        await client.send_message(DATABASE_ID, "✅ Test dari Pyrogram bot.")
        await message.reply("✅ Pesan dikirim ke channel.")
    except Exception as e:
        await message.reply(f"❌ Gagal kirim: {e}")
        print(f"[ERROR] Kirim channel: {e}")

app.run()

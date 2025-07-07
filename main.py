from pyrogram import Client, filters
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")  # bisa @username atau -100...
CHANNEL_INVITE_LINK = os.environ.get("CHANNEL_INVITE_LINK")  # opsional

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


async def main():
    print("🚦 Bot sedang start...")
    await app.start()

    # Coba kenalin channel
    try:
        if CHANNEL_INVITE_LINK:
            print(f"🔗 Join channel dari invite link: {CHANNEL_INVITE_LINK}")
            await app.join_chat(CHANNEL_INVITE_LINK)
        else:
            print(f"🔍 Get chat info dari CHANNEL_ID: {CHANNEL_ID}")
            await app.get_chat(CHANNEL_ID)
        print("✅ Channel berhasil dikenali oleh bot.")
    except Exception as e:
        print(f"❌ Gagal kenalin channel: {e}")

    await app.idle()
    await app.stop()
    print("🛑 Bot dimatikan.")


import asyncio
asyncio.run(main())

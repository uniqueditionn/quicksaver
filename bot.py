import os
import re
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========================
# BOT SETTINGS
# ========================
TOKEN = "8071409829:AAGDLYXJzMiI2u8NAzF4RpOW1zfobEtJLIY"
CHANNEL_USERNAME = "@Arx_0201"

# ========================
# START COMMAND
# ========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)

        if member.status in ["left", "kicked"]:
            await update.message.reply_text(
                f"👋 Hi {user.first_name}!\n\n"
                f"To use this bot, you must first join our channel:\n"
                f"{CHANNEL_USERNAME}\n\n"
                f"After joining, press /start again ✅"
            )
            return

    except Exception:
        await update.message.reply_text(
            f"⚠️ Error: Make sure I’m an **Admin** in {CHANNEL_USERNAME}"
        )
        return

    await update.message.reply_text(
        f"✅ Welcome {user.first_name}!\n\nSend me a YouTube, Instagram, or Facebook link and I’ll download it for you 🚀"
    )

# ========================
# DOWNLOADER
# ========================

async def downloader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not re.match(r'(https?://[^\s]+)', url):
        await update.message.reply_text("⚠️ Please send a valid link.")
        return

    await update.message.reply_text("⏳ Downloading... Please wait.")

    try:
        ydl_opts = {
            "format": "mp4",
            "outtmpl": "downloaded_video.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Telegram max file size (50MB on free accounts)
        file_size = os.path.getsize(filename)
        if file_size > 50 * 1024 * 1024:
            await update.message.reply_text("⚠️ File is too large for Telegram free upload (50MB limit).")
            os.remove(filename)
            return

        # Send video
        await update.message.reply_video(video=open(filename, "rb"), caption=f"✅ {info.get('title', 'Video')}")

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# ========================
# MAIN
# ========================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, downloader))

    app.run_polling()

if __name__ == "__main__":
    main()

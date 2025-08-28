import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Get bot token from environment
TOKEN = os.getenv("8071409829:AAEmziwRFq3JiI9Z88EvgwHpw_FWhSsv_WM")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Welcome to QuickSaver!\n\n"
        "Send me a YouTube, Instagram, or Facebook link and I’ll download it for you. 🎥"
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("⏳ Downloading... please wait!")

    try:
        ydl_opts = {"outtmpl": "video.%(ext)s", "format": "best[ext=mp4]"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, "rb") as f:
            await update.message.reply_video(f, caption="✅ Saved by QuickSaver")

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("🚀 QuickSaver is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

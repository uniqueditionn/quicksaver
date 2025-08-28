import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Bot Token (from Render env)
TOKEN = os.getenv("8071409829:AAHL4q3_hmduCBeaCLibFH45pujW-UaG_vg")

# Your channel username (include @)
CHANNEL_ID = "@Arx_0201"   # 🔴 Replace with your channel username, e.g. @QuickSaverUpdates


# ✅ Function: Check if user is subscribed
async def is_subscribed(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ✅ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if await is_subscribed(user_id, context):
        await update.message.reply_text(
            "✅ Welcome to *QuickSaver*!\n\n"
            "Send me a YouTube, Instagram, or Facebook link and I’ll download it for you. 🎥",
            parse_mode="Markdown"
        )
    else:
        # Show a join button
        keyboard = [[InlineKeyboardButton("👉 Join Channel", url=f"https://t.me/{CHANNEL_ID[1:]}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "❌ To use this bot, you must join our channel first!",
            reply_markup=reply_markup
        )


# ✅ Download video function
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if not await is_subscribed(user_id, context):
        keyboard = [[InlineKeyboardButton("👉 Join Channel", url=f"https://t.me/{CHANNEL_ID[1:]}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "❌ Please join our channel to use this bot!",
            reply_markup=reply_markup
        )
        return

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


# ✅ Main
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("🚀 QuickSaver is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

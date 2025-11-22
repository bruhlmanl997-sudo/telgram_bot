import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "8095099337:AAEYdyPzxa3JY5VMxbHCO0o7q2PlVwtVoJI"

async def youtube_to_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text

    if not text.startswith("http"):
        await message.reply_text("أرسل رابط يوتيوب صحيح يا برو 🎬")
        return

    await message.reply_text("لحظة برو، نحمل الفيديو ونحوّله لأوديو... 🎧")

    # إعدادات التحويل
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([text])

        await message.reply_audio(open("audio.mp3", "rb"))
        os.remove("audio.mp3")

    except Exception as e:
        await message.reply_text(f"صار خطأ يا برو: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), youtube_to_audio))
app.run_polling()

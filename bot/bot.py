import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")  # Your FastAPI server

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Vibie! Use /play <song name> to start a stream.")

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /play <song name>")
        return

    song_name = " ".join(context.args)
    user_id = str(update.effective_user.id)

    response = requests.post(f"{BACKEND_URL}/stream/create", json={
        "user_id": user_id,
        "song": song_name
    })

    if response.status_code != 200:
        await update.message.reply_text("Failed to create stream.")
        return

    stream_data = response.json()
    join_url = stream_data.get("join_url")

    keyboard = [
        [InlineKeyboardButton("Join Stream", url=join_url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Streaming '{song_name}'\nClick below to join:",
        reply_markup=reply_markup
    )

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))

    print("Telegram bot running...")
    app.run_polling()
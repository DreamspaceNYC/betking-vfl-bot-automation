import logging
from telegram import Application
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Telegram Bot Token (Make sure it's stored securely)
import os
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Start command function
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("✅ Hello! Your bot is now active and working!")

# Basic message handler
async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"You said: {update.message.text}")

def main():
    """Start the bot"""
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))

    # Message Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
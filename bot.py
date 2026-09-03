import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
SHOP_API_KEY = os.environ["SHOP_API_KEY"]

BASE_URL = "https://new-bot-gemini-link.onrender.com/shop-api/v1"

HEADERS = {
    "X-Shop-API-Key": SHOP_API_KEY,
    "Authorization": f"Bearer {SHOP_API_KEY}",
}


def api_get(endpoint):
    r = requests.get(
        BASE_URL + endpoint,
        headers=HEADERS,
        timeout=30
    )
    r.raise_for_status()
    return r.json()


def api_post(endpoint, data):
    r = requests.post(
        BASE_URL + endpoint,
        headers={
            **HEADERS,
            "Content-Type": "application/json"
        },
        json=data,
        timeout=60
    )
    r.raise_for_status()
    return r.json()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛍 Products", callback_data="products")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("📦 My Orders", callback_data="orders")],
    ]

    await update.message.reply_text(
        "🛒 Welcome to Nexvora Shop!\n\n"
        "Choose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "balance":
        try:
            data = api_get("/me")

            await query.edit_message_text(
                f"💰 Your Balance\n\n"
                f"{data}"
            )
        except Exception as e:
            await query.edit_message_text(
                f"❌ Error: {e}"
            )

    elif query.data == "products":
        try:
            data = api_get("/products")

            await query.edit_message_text(
                "🛍 Products\n\n"
                f"{data}"
            )
        except Exception as e:
            await query.edit_message_text(
                f"❌ Error: {e}"
            )

    elif query.data == "orders":
        try:
            data = api_get("/orders")

            await query.edit_message_text(
                "📦 Orders\n\n"
                f"{data}"
            )
        except Exception as e:
            await query.edit_message_text(
                f"❌ Error: {e}"
            )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
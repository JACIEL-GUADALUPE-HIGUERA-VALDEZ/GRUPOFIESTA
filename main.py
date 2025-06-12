from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ChatJoinRequestHandler,
    CallbackQueryHandler,
)
from flask import Flask
import asyncio
import logging

TOKEN = "7829297226:AAFkcichy6VgzbVZI_lx4KlTse5pG0Q5D1A"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot corriendo correctamente ✅"

async def run_bot():
    app_telegram = ApplicationBuilder().token(TOKEN).build()

    async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.chat_join_request.from_user

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 COMPRAR ACCESO", url="https://t.me/Fiesta_p_bot")],
            [InlineKeyboardButton("🤝 COMPARTIDO 0/3", url="https://t.me/+I-0yDLYSOk4xNDZh")],
            [InlineKeyboardButton("🎁 PRUEBA GRATIS", callback_data="prueba_gratis")]
        ])

        await context.bot.send_message(
            chat_id=user.id,
            text="👋 Bienvenido al grupo privado. Antes de continuar, elige una opción:",
            reply_markup=keyboard
        )

    async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        data = query.data

        if data == "prueba_gratis":
            await query.answer(
                text="⚠️LAMENTABLEMENTE EL GRUPO DE PRUEBAS ESTÁ ACTUALMENTE FUERA DE LÍNEA POR ALGUNOS INCONVENIENTES, ESPERAMOS PRONTO TENERLO NUEVAMENTE ACTIVO⚠️",
                show_alert=True
            )

    app_telegram.add_handler(ChatJoinRequestHandler(handle_join_request))
    app_telegram.add_handler(CallbackQueryHandler(handle_callback))

    await app_telegram.initialize()
    await app_telegram.start()
    await app_telegram.updater.start_polling()
    await app_telegram.updater.wait_for_stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host="0.0.0.0", port=10000)

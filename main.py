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
import threading

TOKEN = "7829297226:AAFkcichy6VgzbVZI_lx4KlTse5pG0Q5D1A"

# Configurar logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot corriendo correctamente ✅"

# Lógica del bot Telegram
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    logger.info(f"🔔 NUEVA SOLICITUD de {user.full_name} (ID: {user.id})")

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
            text="⚠️LAMENTABLEMENTE EL GRUPO DE PRUEBAS ESTÁ ACTUALMENTE FUERA DE LÍNEA...",
            show_alert=True
        )

# Función para iniciar el bot Telegram con asyncio
async def run_bot():
    app_telegram = ApplicationBuilder().token(TOKEN).build()
    app_telegram.add_handler(ChatJoinRequestHandler(handle_join_request))
    app_telegram.add_handler(CallbackQueryHandler(handle_callback))
    await app_telegram.run_polling()

# Ejecutar Flask + Bot
if __name__ == "__main__":
    # Iniciar Flask en un hilo separado
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()
    # Ejecutar el bot Telegram en el hilo principal
    asyncio.run(run_bot())

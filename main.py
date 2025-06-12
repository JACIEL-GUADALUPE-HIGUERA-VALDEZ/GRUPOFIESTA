from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton  
from telegram.ext import (  
    ApplicationBuilder,  
    ContextTypes,  
    ChatJoinRequestHandler,  
    CallbackQueryHandler,  
)
from flask import Flask
import logging
import asyncio
import os
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

# Función principal del bot
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

    logger.info("✅ Bot de Telegram iniciado correctamente")
    await app_telegram.run_polling()

# Función que ejecuta Flask y Telegram en paralelo
def start_all():
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()
    asyncio.run(run_bot())

if __name__ == "__main__":
    start_all()

import telebot
from telebot import types
import time

TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL_ID = -1003511706384

bot = telebot.TeleBot(TOKEN)

# Kino kodlari
MOVIES = {
    "1": [9, 11, 12, 13, 14, 15],
    "2": [16],
    "3": [40, 41, 42]
}

# START
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Xush kelibsiz! Kino kodini yuboring."
    )

# KINO KOD (Obunasiz)
@bot.message_handler(content_types=['text'])
def movie(message):
    code = message.text.strip()

    if code in MOVIES:
        bot.send_message(message.chat.id, f"🎬 '{code}' kodli kino yuborilmoqda...")
        
        for post_id in MOVIES[code]:
            try:
                bot.copy_message(message.chat.id, CHANNEL_ID, post_id)
                time.sleep(0.5)
            except Exception as e:
                print(f"Xatolik: {e}")
                continue
    else:
        bot.send_message(message.chat.id, "❌ Bunday kodli kino topilmadi.")

print("Bot obuna tekshiruvsiz ishga tushdi...")
bot.infinity_polling()

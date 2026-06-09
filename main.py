import telebot
from telebot import types
import time

TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL_ID = -1003511706384
CHANNEL_LINK = "https://t.me/clipzXorg"

bot = telebot.TeleBot(TOKEN)

# ⚠️ MUHIM: Shu ro'yxatni kanaligizdagi barcha qismlar IDsi bilan to'ldirib chiqing
MOVIES = {
    "1": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 
    "2": [20, 21, 22, 23, 24],
    "3": [40, 41, 42]
}

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Kino kodini yuboring.")

@bot.message_handler(content_types=['text'])
def send_video(message):
    user_id = message.from_user.id
    kod = message.text.strip()

    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Kanalga obuna bo'lish 📢", url=CHANNEL_LINK))
        bot.send_message(message.chat.id, "❌ Botdan foydalanish uchun kanalimizga obuna bo'ling!", reply_markup=markup)
        return

    if kod in MOVIES:
        bot.send_message(message.chat.id, f"✅ '{kod}' kodli barcha qismlar yuborilmoqda...")
        for post_id in MOVIES[kod]:
            try:
                bot.copy_message(message.chat.id, CHANNEL_ID, post_id)
                time.sleep(0.6) # Xabarlar tartib bilan ketishi uchun
            except Exception as e:
                print(f"Xatolik: {e}")
                continue
    else:
        bot.reply_to(message, "❌ Bunday kodli kino topilmadi.")

bot.infinity_polling()

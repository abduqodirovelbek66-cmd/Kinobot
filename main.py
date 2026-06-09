import telebot
from telebot import types
import time

# ⚠️ Sozlamalar
TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL_ID = -1003511706384
CHANNEL_LINK = "https://t.me/clipzXorg"

bot = telebot.TeleBot(TOKEN)

# Kino qismlari (Kanalidagi post ID'larini shu yerga yozing)
# Bot har safar kanalni skanerlamasligi uchun bu eng ishonchli usul
MOVIES = {
    "1": [5, 6, 7, 8, 9],    
    "11": [12, 13, 14],     
    "2": [20, 21]           
}

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        # Faqat kanalga obuna bo'lgan bo'lsa True qaytaradi
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

    # 1. Obuna tekshiruvi
    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Kanalga obuna bo'lish 📢", url=CHANNEL_LINK))
        bot.send_message(message.chat.id, "❌ Botdan foydalanish uchun kanalimizga obuna bo'ling!", reply_markup=markup)
        return

    # 2. Kinoni yuborish
    if kod in MOVIES:
        bot.reply_to(message, f"✅ '{kod}' kodli kino yuborilmoqda...")
        for post_id in MOVIES[kod]:
            try:
                bot.copy_message(message.chat.id, CHANNEL_ID, post_id)
                time.sleep(0.5) 
            except Exception as e:
                print(f"Xatolik: {e}")
                continue
    else:
        bot.reply_to(message, "❌ Bunday kino topilmadi.")

print("Bot ishga tushdi...")
bot.infinity_polling()

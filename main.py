import telebot
from telebot import types
import time

# ⚠️ Sozlamalar
TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL_ID = -1003511706384
CHANNEL_LINK = "https://t.me/clipzXorg"
ADMINS = [8217118208, 8359977081] 

bot = telebot.TeleBot(TOKEN)

# Kino qismlari
MOVIES = {
    "1": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],    
    "2": [20, 21, 22, 23, 24],     
    "3": [40, 41, 42]           
}

# --- Obuna tekshirish funksiyasi (O'zgartirilmadi, faqat ishlashi ta'minlandi) ---
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        # Agar bot admin bo'lsa, bu status qaytaradi
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return False

def get_sub_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Kanalga o'tish 📢", url=CHANNEL_LINK))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Start bosganda ham obuna tekshiriladi
    if is_subscribed(message.from_user.id):
        bot.reply_to(message, "✅ Obuna tasdiqlandi! Kino kodini yuboring.")
    else:
        bot.send_message(message.chat.id, "❌ Botdan foydalanish uchun kanalimizga obuna bo'ling!", reply_markup=get_sub_markup())

@bot.message_handler(content_types=['text'])
def send_video(message):
    # --- ASOSIY O'ZGARISH SHU YERDA: Obuna tekshiruvi ---
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Obuna bo'lmaganingiz uchun kinoni yubora olmayman. Iltimos, kanalimizga obuna bo'ling:", reply_markup=get_sub_markup())
        return

    kod = message.text.strip()
    
    if kod in MOVIES:
        bot.reply_to(message, "⏳ Kino qismlari yuborilmoqda...")
        for post_id in MOVIES[kod]:
            try:
                bot.copy_message(message.chat.id, CHANNEL_ID, post_id)
                time.sleep(0.5) 
            except:
                continue
    else:
        bot.reply_to(message, "❌ Bunday kino topilmadi.")

print("Bot ishga tushdi...")
bot.infinity_polling()

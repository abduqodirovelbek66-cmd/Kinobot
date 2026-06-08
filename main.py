import telebot
from telebot import types
import time

# ⚠️ Sozlamalar
TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL_ID = -1003511706384 
CHANNEL_LINK = "https://t.me/clipzXorg"
ADMINS = [8217118208, 8359977081] 

bot = telebot.TeleBot(TOKEN)

# Kino qismlari (Kanalidagi post ID'larini shu yerga to‘g‘ri kiriting)
MOVIES = {
    "1": [5, 6, 7, 8, 9],    
    "11": [12, 13, 14],     
    "2": [20, 21]           
}

def is_subscribed(user_id):
    try:
        # Kanalga obunani tekshirish
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def get_sub_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Kanalga o‘tish 📢", url=CHANNEL_LINK))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Kino kodini yuboring (masalan: 1, 11 yoki 2).")

@bot.message_handler(content_types=['text'])
def send_video(message):
    # 1. Obunani tekshirish (Agar obuna bo‘lmasa, hech narsa topmaydi va xabar chiqadi)
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Botdan foydalanish uchun avval kanalimizga obuna bo‘ling!", reply_markup=get_sub_markup())
        return

    kod = message.text.strip()
    
    # 2. Kodni tekshirish
    if kod in MOVIES:
        bot.reply_to(message, f"✅ {kod}-kodli kino qismlari yuborilmoqda...")
        # 3. Qismlarni ketma-ket yuborish
        for post_id in MOVIES[kod]:
            try:
                bot.copy_message(message.chat.id, CHANNEL_ID, post_id)
                time.sleep(0.7) # Ketma-ketlik uchun ozgina pauza
            except Exception as e:
                print(f"Xatolik: {e}")
                bot.send_message(message.chat.id, f"❌ {post_id}-qismni yuborishda xatolik yuz berdi.")
                continue
    else:
        bot.reply_to(message, "❌ Bunday kodli kino topilmadi.")

print("Bot ishga tushdi...")
bot.infinity_polling()

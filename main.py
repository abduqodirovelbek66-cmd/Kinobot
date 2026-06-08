import telebot
from telebot import types
import time

# ⚠️ Sozlamalar
TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL_ID = -1003511706384 # Kanal ID'sini shu yerga yozing
CHANNEL_LINK = "https://t.me/clipzXorg"
ADMINS = [8217118208, 8359977081] 

bot = telebot.TeleBot(TOKEN)

# 🎬 KINO KODLARI VA ULARNING QISMLARI (ID raqamlari)
# Har bir kino uchun qismlarni list [ ] ichida ketma-ket yozib chiqing
MOVIES = {
    "1": [5, 6, 7, 8, 9],    # 1-kodli kinoning 5 ta qismi
    "11": [12, 13, 14],     # 11-kodli kinoning 3 ta qismi
    "2": [20, 21]           # 2-kodli kinoning qismlari
}

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def get_sub_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Kanalga o'tish 📢", url=CHANNEL_LINK))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_subscribed(message.from_user.id):
        bot.reply_to(message, "✅ Obuna tasdiqlandi! \n\n🎬 Kino kodini yuboring (masalan: 1 yoki 11).")
    else:
        bot.send_message(message.chat.id, "❌ Botdan foydalanish uchun kanalimizga obuna bo'ling!", reply_markup=get_sub_markup())

@bot.message_handler(content_types=['text'])
def send_video(message):
    # Obunani tekshirish
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Obuna bo'ling!", reply_markup=get_sub_markup())
        return

    kod = message.text.strip()
    
    # Aniq qidiruv (1 yozilganda 11 chiqib ketmaydi)
    if kod in MOVIES:
        bot.reply_to(message, f"🎬 '{kod}' kodli kino qismlari yuborilmoqda...")
        
        # Ro'yxatdagi barcha qismlarni tartib bilan yuborish
        for post_id in MOVIES[kod]:
            try:
                bot.copy_message(message.chat.id, CHANNEL_ID, post_id)
                time.sleep(0.8) # Telegram ban bermasligi uchun pauza
            except Exception as e:
                bot.send_message(message.chat.id, f"⚠️ {post_id}-qismni yuborishda xatolik yuz berdi.")
    else:
        bot.reply_to(message, "❌ Bunday kodli kino topilmadi.")

print("Bot mukammal tartibda ishga tushdi...")
bot.infinity_polling()

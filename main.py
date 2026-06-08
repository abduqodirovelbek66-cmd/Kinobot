import telebot
from telebot import types

# ⚠️ Sozlamalar
TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL_ID = -1003511706384 # Kanal ID'sini shu yerga yozing
CHANNEL_LINK = "https://t.me/clipzXorg"
ADMINS = [8217118208, 8359977081] # O'z ID raqamingizni kiriting

bot = telebot.TeleBot(TOKEN)

# 🎬 KINO KODLARI (Bu yerda kod: xabar_id ko'rinishida saqlanadi)
MOVIES = {
    "1": 5,  # 1-kodli kino, kanalning 5-xabari
    "2": 12  # 2-kodli kino, kanalning 12-xabari
}

def is_subscribed(user_id):
    """Obunani tekshirish"""
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
        bot.reply_to(message, "✅ Obuna tasdiqlandi! \n\n🎬 Kino kodini yuboring.")
    else:
        bot.send_message(message.chat.id, "❌ Botdan foydalanish uchun kanalimizga obuna bo'ling!", reply_markup=get_sub_markup())

@bot.message_handler(commands=['add'])
def add_movie_command(message):
    """Adminlar uchun kino qo'shish qoidasini ko'rsatish"""
    if message.from_user.id in ADMINS:
        bot.reply_to(message, "Yangi kino qo'shish uchun kod va xabar ID sini quyidagicha yozing:\n/add_kod 123:45")

@bot.message_handler(commands=['add_kod'])
def add_movie(message):
    """Kino kodini bazaga (MOVIES) qo'shish"""
    if message.from_user.id in ADMINS:
        try:
            data = message.text.split()[1].split(':')
            code, post_id = data[0], int(data[1])
            MOVIES[code] = post_id
            bot.reply_to(message, f"✅ Saqlandi! Kod: {code}, Xabar ID: {post_id}")
        except:
            bot.reply_to(message, "❌ Xatolik! Yozilish tartibi: /add_kod 1:123")

@bot.message_handler(content_types=['text'])
def send_video(message):
    user_id = message.from_user.id
    
    if not is_subscribed(user_id):
        bot.send_message(message.chat.id, "❌ Iltimos, kanalimizga obuna bo'ling:", reply_markup=get_sub_markup())
        return
    
    kod = message.text.strip()
    if kod in MOVIES:
        try:
            bot.copy_message(message.chat.id, CHANNEL_ID, MOVIES[kod])
        except:
            bot.reply_to(message, "❌ Video topilmadi yoki bot kanal admini emas.")
    else:
        bot.reply_to(message, "❌ Bu kod bilan kino topilmadi.")

print("Bot admin paneli bilan ishga tushdi...")
bot.infinity_polling()

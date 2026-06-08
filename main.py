import telebot
from telebot import types
import sqlite3
import time

# ⚠️ Sozlamalar
TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL_ID = "@clipzXorg" 
CHANNEL_LINK = "https://t.me/clipzXorg"
# Adminlar ID ro'yxati (o'zingiz va sherigingiz ID raqamlarini yozing)
ADMINS = [8217118208, 8359977081] 

bot = telebot.TeleBot(TOKEN)

def is_subscribed(user_id):
    """Obunani tekshirish"""
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def init_db():
    conn = sqlite3.connect('bazam.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS videolar (id INTEGER PRIMARY KEY AUTOINCREMENT, kod TEXT, file_id TEXT, izoh TEXT)")
    conn.commit()
    conn.close()

init_db()

# Kanalga o'tish tugmasi
def get_sub_markup():
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Kanalga o'tish 📢", url=CHANNEL_LINK)
    markup.add(button)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Obunani tekshirish
    if is_subscribed(message.from_user.id):
        bot.reply_to(message, "✅ Obuna tasdiqlandi! \n\n🎬 Endi menga kino kodini yuborishingiz mumkin.")
    else:
        bot.send_message(message.chat.id, "❌ Botdan foydalanish uchun kanalimizga obuna bo'ling!", reply_markup=get_sub_markup())

@bot.message_handler(content_types=['video'])
def add_video(message):
    if message.from_user.id in ADMINS:
        if message.caption:
            lines = message.caption.split('\n')
            kod = lines[0].strip()
            kino_nomi = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
            file_id = message.video.file_id
            
            conn = sqlite3.connect('bazam.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO videolar (kod, file_id, izoh) VALUES (?, ?, ?)", (kod, file_id, kino_nomi))
            conn.commit()
            conn.close()
            bot.reply_to(message, f"✅ Saqlandi!\n🔑 Kod: {kod}")
        else:
            bot.reply_to(message, "❌ Izoh yozish qolib ketdi!")

@bot.message_handler(content_types=['text'])
def send_video(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Iltimos, kanalimizga obuna bo'ling:", reply_markup=get_sub_markup())
        return

    kod = message.text.strip()
    conn = sqlite3.connect('bazam.db')
    cursor = conn.cursor()
    cursor.execute("SELECT file_id, izoh FROM videolar WHERE kod = ?", (kod,))
    results = cursor.fetchall()
    conn.close()
    
    if results:
        for row in results:
            bot.send_video(message.chat.id, row[0], caption=row[1] if row[1] else "")
            time.sleep(0.5)
    else:
        bot.reply_to(message, "❌ Video topilmadi.")

print("Bot 2 ta admin va tasdiqlash funksiyasi bilan ishga tushdi...")
bot.infinity_polling()

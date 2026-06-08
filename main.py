import telebot
import sqlite3
import time

# ⚠️ Konfiguratsiya
TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
# Kanalingiz useri (masalan: @clipzXorg)
CHANNEL_ID = "@clipzXorg" 
ADMINS = [8217118208, 8359977081] # IDlaringizni shu yerga yozing

bot = telebot.TeleBot(TOKEN)

def is_subscribed(user_id):
    """Foydalanuvchi kanalda borligini tekshirish"""
    try:
        # Bot kanalda admin bo'lishi shart!
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        # status: creator, administrator yoki member bo'lsa - obuna bo'lgan
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return False

# Baza yaratish funksiyasi
def init_db():
    conn = sqlite3.connect('bazam.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS videolar (id INTEGER PRIMARY KEY AUTOINCREMENT, kod TEXT, file_id TEXT, izoh TEXT)")
    conn.commit()
    conn.close()

init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Kanalni tekshirish
    if not is_subscribed(message.from_user.id):
        bot.reply_to(message, f"❌ Botdan foydalanish uchun kanalimizga obuna bo'ling: https://t.me/clipzXorg\n\nObuna bo'lgach /start buyrug'ini qayta bosing.")
        return
    
    bot.reply_to(message, "👋 Assalomu alaykum! Kino kodini yuboring.")

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
            bot.reply_to(message, f"✅ Muvaffaqiyatli saqlandi!\n🔑 Kod: {kod}")
        else:
            bot.reply_to(message, "❌ Izoh yozish qolib ketdi!")

@bot.message_handler(content_types=['text'])
def send_video(message):
    # Kanalni tekshirish
    if not is_subscribed(message.from_user.id):
        bot.reply_to(message, f"❌ Iltimos, kanalimizga obuna bo'ling: https://t.me/clipzXorg")
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

print("Bot 2 ta admin va kanal tekshiruvi bilan ishga tushdi...")
bot.infinity_polling()

import telebot
import sqlite3
import time

TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL_ID = "@clipzXorg"  # Kanal useri
CHANNEL_LINK = "https://t.me/clipzXorg"
ADMINS = [8217118208, 8359977081] 

bot = telebot.TeleBot(TOKEN)

def is_subscribed(user_id):
    """Obunani tekshirish (Bot kanal admini bo'lishi shart)"""
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        # Statuslar: creator, administrator yoki member
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Xatolik: {e}")
        return False

# --- Xabar yuborish funksiyasi (Linkni yashirish uchun) ---
def send_sub_message(chat_id):
    text = f"❌ Botdan foydalanish uchun avval kanalimizga obuna bo'ling!\n\n👉 [Kanal]( {CHANNEL_LINK} )"
    bot.send_message(chat_id, text, parse_mode='Markdown')

def init_db():
    conn = sqlite3.connect('bazam.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS videolar (id INTEGER PRIMARY KEY AUTOINCREMENT, kod TEXT, file_id TEXT, izoh TEXT)")
    conn.commit()
    conn.close()

init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not is_subscribed(message.from_user.id):
        send_sub_message(message.chat.id)
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
            bot.reply_to(message, f"✅ Saqlandi: {kod}")
        else:
            bot.reply_to(message, "❌ Izoh yozish qolib ketdi!")

@bot.message_handler(content_types=['text'])
def send_video(message):
    if not is_subscribed(message.from_user.id):
        send_sub_message(message.chat.id)
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

bot.infinity_polling()

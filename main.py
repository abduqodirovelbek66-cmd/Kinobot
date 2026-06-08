import telebot
import sqlite3
import time
import os

# Tokenni Render muhitidan o'qish (xavfsizroq)
TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
bot = telebot.TeleBot(TOKEN)

# Admin ID
ADMIN_ID = 8217118208

def init_db():
    """Bot papkasida bazani yaratish"""
    conn = sqlite3.connect('bazam.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videolar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kod TEXT,
        file_id TEXT,
        izoh TEXT
    )
    """)
    conn.commit()
    conn.close()

# Bot ishga tushganda bazani tayyorlaydi
init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "👋 Assalomu alaykum! Kino botga xush kelibsiz.\n\n🎬 Menga kino kodini yuboring!"
    if message.from_user.id == ADMIN_ID:
        welcome_text += "\n\n⚙️ Admin, video saqlash uchun:\n1-qatorga: kodni yozing\n2-qatorga: kino nomini yozing!"
    bot.reply_to(message, welcome_text)

@bot.message_handler(content_types=['video'])
def add_video(message):
    if message.from_user.id == ADMIN_ID:
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
            
            bot.reply_to(message, f"✅ Muvaffaqiyatli saqlandi!\n\n🔑 Kod: {kod}\n🎬 Kino nomi: {kino_nomi}")
        else:
            bot.reply_to(message, "❌ Videoga izoh (kod va qism nomi) yozish qolib ketdi!")

@bot.message_handler(content_types=['text'])
def send_video(message):
    kod = message.text.strip()
    if kod == "/start": return

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
        bot.reply_to(message, f"❌ '{kod}' kodli video topilmadi.")

print("Bot SQLite bazasida muvaffaqiyatli ishga tushdi...")
bot.infinity_polling()

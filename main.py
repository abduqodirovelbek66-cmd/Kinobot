import os
import psycopg2
import telebot
import time

# ⚠️ Bot tokeningizni shu yerga yozing!
TOKEN = "8625467620:AAEWlGHoWJJ-spX_1QPrEVqXcTAFvnCOOuA"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8217118208

# ⚠️ Supabase'dan olgan URI manzilingizni mana shu yerga qo'ying!
DB_URI = "postgresql://postgres:PAROLINGIZ@db.xxxxxx.supabase.co:5432/postgres"

def init_db():
    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videolar (
        kod TEXT,
        file_id TEXT,
        izoh TEXT
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "👋 Assalomu alaykum! Kino botga xush kelibsiz.\n\n🎬 Menga kodni yuboring!"
    if message.from_user.id == ADMIN_ID:
        welcome_text += "\n\n⚙️ Admin, video saqlash uchun:\n1-qatorga: kodni yozing\n2-qatorga: kino nomini yozing!"
    bot.reply_to(message, welcome_text)

@bot.message_handler(content_types=['video'])
def add_video(message):
    if message.from_user.id == ADMIN_ID:
        if message.caption:
            lines = message.caption.split('\n')
            kod = lines[0].strip() 
            
            if len(lines) > 1:
                kino_nomi = "\n".join(lines[1:]).strip()
            else:
                kino_nomi = "Nomsiz kino"
            
            file_id = message.video.file_id
            
            conn = psycopg2.connect(DB_URI)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO videolar (kod, file_id, izoh) VALUES (%s, %s, %s)", (kod, file_id, kino_nomi))
            conn.commit()
            cursor.close()
            conn.close()
            
            bot.reply_to(message, f"✅ Muvaffaqiyatli saqlandi!\n\n🔑 Kod: {kod}\n🎬 Kino nomi: {kino_nomi}")
        else:
            bot.reply_to(message, "❌ Videoga izoh yozish qolib ketdi!")

@bot.message_handler(content_types=['text'])
def send_video(message):
    kod = message.text.strip()
    if kod == "/start":
        return

    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()
    cursor.execute("SELECT file_id, izoh FROM videolar WHERE kod = %s", (kod,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if results:
        for row in results:
            video_id = row[0]
            video_izoh = row[1]
            bot.send_video(message.chat.id, video_id, caption=video_izoh)
            time.sleep(1)
    else:
        bot.reply_to(message, f"❌ '{kod}' kodli video topilmadi.")

print("Bot bulutli (PostgreSQL) bazada umrbod rejimda ishga tushdi...")
bot.infinity_polling()

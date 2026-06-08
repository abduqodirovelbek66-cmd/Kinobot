import psycopg2
import telebot
import time

# ⚠️ Bot tokeningizni BotFather'dan olib, shu yerga yozing!
TOKEN = "8625467620:AAEWlGHoWJJ-spX_1QPrEVqXcTAFvnCOOuA"
bot = telebot.TeleBot(TOKEN)

# ⚠️ Sizning telegram ID raqamingiz (Faqat siz video yuklay olasiz)
ADMIN_ID = 8217118208

# ⚠️ Supabase yoki Neon.tech saytidan olgan bepul PostgreSQL URI manzilingizni shu yerga qo'ying!
# Bu havola tufayli bot ichidagi kinolar 1 yillab ham o'chib ketmaydi.
DB_URI = "postgresql://postgres:PAROLINGIZ@db.xxxxxx.supabase.co:5432/postgres"

def init_db():
    """Bulutli bazada kino jadvallarini yaratish"""
    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videolar (
        id SERIAL PRIMARY KEY,
        kod TEXT,
        file_id TEXT,
        izoh TEXT
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Bot yonganda bazani srazu tekshiradi
init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Botga start bosgandagi toza, reklamasiz xabar"""
    welcome_text = "👋 Assalomu alaykum! Kino botga xush kelibsiz.\n\n🎬 Menga kino kodini yuboring!"
    if message.from_user.id == ADMIN_ID:
        welcome_text += "\n\n⚙️ Admin, video saqlash uchun:\n1-qatorga: kodni yozing\n2-qatorga: kino nomini yozing!"
    bot.reply_to(message, welcome_text)

@bot.message_handler(content_types=['video'])
def add_video(message):
    """Admin video yuborganda uni bulutli bazaga umrbod saqlash"""
    if message.from_user.id == ADMIN_ID:
        if message.caption:
            # Matnni qatorlarga ajratamiz (Enter bosilgan joyidan)
            lines = message.caption.split('\n')
            kod = lines[0].strip() 
            
            # Agar 2-qatorda nom yozilgan bo'lsa, uni saqlaydi
            if len(lines) > 1:
                kino_nomi = "\n".join(lines[1:]).strip()
            else:
                kino_nomi = "" 
            
            file_id = message.video.file_id
            
            # Supabase bazasiga yozish
            conn = psycopg2.connect(DB_URI)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO videolar (kod, file_id, izoh) VALUES (%s, %s, %s)", (kod, file_id, kino_nomi))
            conn.commit()
            cursor.close()
            conn.close()
            
            bot.reply_to(message, f"✅ Muvaffaqiyatli saqlandi!\n\n🔑 Kod: {kod}\n🎬 Kino nomi: {kino_nomi}")
        else:
            bot.reply_to(message, "❌ Videoga izoh (kod va qism nomi) yozish qolib ketdi!")

@bot.message_handler(content_types=['text'])
def send_video(message):
    """Foydalanuvchi kod yozganda kinoni toza holatda (kodisiz) qaytarish"""
    kod = message.text.strip()
    if kod == "/start":
        return

    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()
    # Kodga tegishli barcha videolarni joylangan tartibida oladi
    cursor.execute("SELECT file_id, izoh FROM videolar WHERE kod = %s ORDER BY id ASC", (kod,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if results:
        for row in results:
            video_id = row[0]
            video_izoh = row[1]
            
            # Foydalanuvchiga videoni faqat o'z nomi bilan (kodisiz) yuboradi
            if video_izoh:
                bot.send_video(message.chat.id, video_id, caption=video_izoh)
            else:
                bot.send_video(message.chat.id, video_id)
            time.sleep(1) # Blokirovkaga tushmaslik uchun 1 soniya pauza
    else:
        bot.reply_to(message, f"❌ '{kod}' kodli video topilmadi.")

print("Bot bulutli bazada mutlaqo reklamasiz va umrbod rejimda ishlamoqda...")
bot.infinity_polling()

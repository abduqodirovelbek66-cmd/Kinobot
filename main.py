import sqlite3
import telebot
import time

# ⚠️ Bot tokeningizni shu yerga qaytadan yozib qo'ying!
TOKEN = "8625467620:AAEWlGHoWJJ-spX_1QPrEVqXcTAFvnCOOuA"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8217118208

def init_db():
    conn = sqlite3.connect("Kino_baza.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videolar (
        kod TEXT,
        file_id TEXT,
        izoh TEXT
    )
    """)
    conn.commit()
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
            # Matnni qatorlarga ajratamiz (Enter bosilgan joyidan)
            lines = message.caption.split('\n')
            
            # 1-qatordagi yozuvni kod qilib olamiz (boshidagi-oxiridagi bo'shliqlarni olib tashlab)
            kod = lines[0].strip() 
            
            # Agar admin 2-qatorga nom yozgan bo'lsa, o'shani kino nomi qilamiz
            if len(lines) > 1:
                kino_nomi = "\n".join(lines[1:]).strip()
            else:
                kino_nomi = "Nomsiz kino" # Agar 2-qatorga hech narsa yozilmagan bo'lsa
            
            file_id = message.video.file_id
            
            conn = sqlite3.connect("Kino_baza.db", check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO videolar (kod, file_id, izoh) VALUES (?, ?, ?)", (kod, file_id, kino_nomi))
            conn.commit()
            conn.close()
            
            # Tasdiqlash xabarida hammasi alohida va toza ko'rinadi!
            bot.reply_to(message, f"✅ Muvaffaqiyatli saqlandi!\n\n🔑 Kod: {kod}\n🎬 Kino nomi: {kino_nomi}")
        else:
            bot.reply_to(message, "❌ Videoga izoh (kod va qism nomi) yozish qolib ketdi!")

@bot.message_handler(content_types=['text'])
def send_video(message):
    kod = message.text.strip()
    if kod == "/start":
        return

    conn = sqlite3.connect("Kino_baza.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT file_id, izoh FROM videolar WHERE kod = ?", (kod,))
    results = cursor.fetchall()
    conn.close()
    
    if results:
        for row in results:
            video_id = row[0]
            video_izoh = row[1] # Bu yerda faqat toza kino nomi turibdi
            bot.send_video(message.chat.id, video_id, caption=video_izoh)
            time.sleep(1)
    else:
        bot.reply_to(message, f"❌ '{kod}' kodli video topilmadi.")

print("Bot mukammal rejimda ishlamoqda...")
bot.infinity_polling()

import sqlite3
import telebot

# ⚠️ Bot tokeningizni shu yerga qaytadan yozib qo'ying!
TOKEN = "8625467620:AAEWlGHoWJJ-spX_1QPrEVqXcTAFvnCOOuA"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8217118208

def init_db():
    conn = sqlite3.connect("Kino_baza.db", check_same_thread=False)
    cursor = conn.cursor()
    # Bazada endi matnni (nomini) ham saqlash uchun 'izoh' ustunini qo'shdik
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videolar (
        kod TEXT PRIMARY KEY,
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
        welcome_text += "\n\n⚙️ Admin, video saqlash uchun tagiga kod va nomini yozib video yuboring."
    bot.reply_to(message, welcome_text)

@bot.message_handler(content_types=['video'])
def add_video(message):
    if message.from_user.id == ADMIN_ID:
        if message.caption:
            # Birinchi so'zni kod qilib oladi (masalan: 01)
            kod = message.caption.split()[0]       
            file_id = message.video.file_id
            # Butun boshli yozilgan matnni (nomini) to'liqligicha saqlaydi
            izoh = message.caption                 
            
            conn = sqlite3.connect("Kino_baza.db", check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO videolar (kod, file_id, izoh) VALUES (?, ?, ?)", (kod, file_id, izoh))
            conn.commit()
            conn.close()
            
            bot.reply_to(message, f"✅ Video '{kod}' kodi va nomi bilan bazaga umrbod saqlandi!")
        else:
            bot.reply_to(message, "❌ Videoga izoh (kod va nom) yozish qolib ketdi!")

@bot.message_handler(content_types=['text'])
def send_video(message):
    kod = message.text
    if kod == "/start":
        return

    conn = sqlite3.connect("Kino_baza.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT file_id, izoh FROM videolar WHERE kod = ?", (kod,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        video_id = result[0]
        video_izoh = result[1] # Saqlangan to'liq nomini oladi
        # Foydalanuvchiga videoni o'z nomi (izohi) bilan qaytaradi
        bot.send_video(message.chat.id, video_id, caption=video_izoh)
    else:
        bot.reply_to(message, f"❌ '{kod}' kodli video topilmadi.")

print("Bot xostingda to'liq ishlamoqda...")
bot.infinity_polling()

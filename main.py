import sqlite3
import telebot

TOKEN = "8625467620:AAEWlGHoWJJ-spX_1QPrEVqXcTAFvnCOOuA"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8217118208

conn = sqlite3.connect("Kino_baza.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS videolar (
    kod TEXT PRIMARY KEY,
    file_id TEXT
)
""")
conn.commit()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "👋 Assalomu alaykum! Kino botga xush kelibsiz.\n\n🎬 Menga kodni yuboring!"
    if message.from_user.id == ADMIN_ID:
        welcome_text += "\n\n⚙️ Admin, video saqlash uchun tagiga kod yozib video yuboring."
    bot.reply_to(message, welcome_text)

@bot.message_handler(content_types=['video'])
def add_video(message):
    if message.from_user.id == ADMIN_ID:
        if message.caption:
            kod = message.caption.split()[0]       
            file_id = message.video.file_id
            cursor.execute("INSERT OR REPLACE INTO videolar (kod, file_id) VALUES (?, ?)", (kod, file_id))
            conn.commit()
            bot.reply_to(message, f"✅ Video '{kod}' kodi bilan bazaga umrbod saqlandi!")
        else:
            bot.reply_to(message, "❌ Videoga izoh yozish qolib ketdi!")

@bot.message_handler(content_types=['text'])
def send_video(message):
    kod = message.text
    cursor.execute("SELECT file_id FROM videolar WHERE kod = ?", (kod,))
    result = cursor.fetchone()
    if result:
        bot.send_video(message.chat.id, result[0], caption=f"🍿 {kod}-video")
    else:
        if kod != "/start":
            bot.reply_to(message, f"❌ '{kod}' kodli video topilmadi.")

print("Bot xostingda ishga tushdi...")
bot.infinity_polling()

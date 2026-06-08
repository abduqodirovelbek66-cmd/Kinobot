import telebot
import time

TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL_ID = -1003511706384 # Kanal ID raqamingiz
CHANNEL_LINK = "https://t.me/clipzXorg"

ADMINS = [8217118208, 8359977081]

bot = telebot.TeleBot(TOKEN)

# Kino qismlari (ID larni kanalga qarab to'g'rilab chiqing)
MOVIES = {
    "1": [5, 6, 7, 8], # Faqat mavjud bo'lgan ID larni yozing!
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎬 Kino kodini yuboring.")

@bot.message_handler(content_types=['text'])
def send_video(message):
    kod = message.text.strip()
    
    if kod in MOVIES:
        # Mavjud qismlarni yuborish
        for post_id in MOVIES[kod]:
            try:
                bot.copy_message(message.chat.id, CHANNEL_ID, post_id)
                time.sleep(0.5)
            except:
                # Agar video o'chib ketgan bo'lsa, xatolik chiqarmasdan o'tkazib yuboradi
                continue 
    else:
        bot.reply_to(message, "❌ Kino topilmadi.")

bot.infinity_polling()

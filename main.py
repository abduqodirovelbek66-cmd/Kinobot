import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL = "@clipzXorg"

bot = telebot.TeleBot(TOKEN)

# Kino bazasi
movies = {
    "1001": "🎬 Kino nomi: Ovchi itlar 2-FASL Barcha qisimlar\n📥 Link: https://t.me/c/3511706384/9",
    "1002": "🎬 Kino nomi: Interstellar\n📥 Link: https://example.com/movie2",
    "1003": "🎬 Kino nomi: Avengers\n📥 Link: https://example.com/movie3"
}

def channel_button():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(
        "📢 KANAL",
        url="https://t.me/clipzXorg"
    )
    markup.add(btn)
    return markup

def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Botimizga xush kelibsiz!\n\n📢 Kanalga obuna bo'ling 😊",
        reply_markup=channel_button()
    )

@bot.message_handler(func=lambda message: True)
def get_movie(message):
    user_id = message.from_user.id

    if not check_sub(user_id):
        bot.reply_to(
            message,
            "📢 Kanalga obuna bo'ling 😊",
            reply_markup=channel_button()
        )
        return

    code = message.text.strip()

    if code in movies:
        bot.reply_to(message, movies[code])
    else:
        bot.reply_to(message, "Kino kodi xato 🚫")

print("Bot ishlayapti...")
bot.infinity_polling()

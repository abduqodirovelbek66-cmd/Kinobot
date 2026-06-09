import telebot

TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL = "@your_channel"

bot = telebot.TeleBot(TOKEN)

# Kino bazasi
movies = {
    "1001": "🎬 Kino nomi: Ovchi Itlar 2 -FASL Barcha qisim\n📥 Link:https://t.me/c/3511706384/9 https://t.me/c/3511706384/10 https://t.me/c/3511706384/11 https://t.me/c/3511706384/12 https://t.me/c/3511706384/13 https://t.me/c/3511706384/14 https://t.me/c/3511706384/15",
    "1002": "🎬 Kino nomi: Interstellar\n📥 Link: https://example.com/movie2",
    "1003": "🎬 Kino nomi: Avengers\n📥 Link: https://example.com/movie3"
}

def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@bot.message_handler(func=lambda message: True)
def get_movie(message):
    user_id = message.from_user.id

    if not check_sub(user_id):
        bot.reply_to(
            message,
            "Kanalga obuna bo'ling 😊"
        )
        return

    code = message.text.strip()

    if code in movies:
        bot.reply_to(message, movies[code])
    else:
        bot.reply_to(message, "Kino kodi xato 🚫")

print("Bot ishlayapti...")
bot.infinity_polling()

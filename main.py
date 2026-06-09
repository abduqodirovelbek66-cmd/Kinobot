import telebot
from telebot import types

TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL_ID = -1003511706384
CHANNEL_LINK = "https://t.me/clipzXorg"

bot = telebot.TeleBot(TOKEN)

# Kino kodlari -> kanal post ID lar
MOVIES = {
    "1": [9, 10, 11, 12, 13, 14, 15],
    "2": [16],
    "3": [40, 41, 42]
}

# OBUNA TEKSHIRISH
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# BUTTONLAR
def join_button():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📢 KANAL", url=CHANNEL_LINK),
        types.InlineKeyboardButton("✅ TEKSHIRISH", callback_data="check")
    )
    return markup


# START
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Xush kelibsiz!\n\n📢 Kino botdan foydalanish uchun kanalga obuna bo‘ling.",
        reply_markup=join_button()
    )


# CHECK BUTTON
@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):

    if is_subscribed(call.from_user.id):
        bot.edit_message_text(
            "✅ Obuna tasdiqlandi!\n🎬 Endi kino kodini yuboring.",
            call.message.chat.id,
            call.message.message_id
        )
    else:
        bot.answer_callback_query(call.id, "❌ Siz hali obuna bo‘lmagansiz!")


# KINO KOD
@bot.message_handler(content_types=['text'])
def movie(message):

    user_id = message.from_user.id
    code = message.text.strip()

    # OBUNA YO'Q BO'LSA
    if not is_subscribed(user_id):
        bot.send_message(
            message.chat.id,
            "❌ Avval kanalga obuna bo‘ling!",
            reply_markup=join_button()
        )
        return

    # KINO BOR BO'LSA
    if code in MOVIES:
        bot.send_message(message.chat.id, f"🎬 '{code}' kodli kino yuborilmoqda...")

        for post_id in MOVIES[code]:
            try:
                bot.copy_message(message.chat.id, CHANNEL_ID, post_id)
            except:
                pass

    else:
        bot.send_message(message.chat.id, "❌ Kino kodi topilmadi")


print("Bot ishlayapti...")
bot.infinity_polling()

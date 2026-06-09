import telebot
from telebot import types
import time

TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL_ID = -1003511706384
CHANNEL_LINK = "https://t.me/clipzXorg"

bot = telebot.TeleBot(TOKEN)

# Kino kodlari
MOVIES = {
    "1": [9, 10, 11, 12, 13, 14, 15],
    "2": [16],
    "3": [40, 41, 42]
}

# --- OBUNA TEKSHIRISH (Qat'iy rejim) ---
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        # Agar status 'left' yoki 'kicked' bo'lsa, obuna bo'lmagan
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except:
        # Agar bot admin bo'lmasa yoki xatolik bo'lsa, False qaytaradi
        return False

# --- BUTTON ---
def join_button():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📢 KANALGA OBUNA BO'LISH", url=CHANNEL_LINK),
        types.InlineKeyboardButton("✅ TEKSHIRISH", callback_data="check")
    )
    return markup

# --- START ---
@bot.message_handler(commands=['start'])
def start(message):
    if is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "✅ Obuna tasdiqlandi! Kino kodini yuboring.")
    else:
        bot.send_message(
            message.chat.id,
            "👋 Xush kelibsiz!\n\n❌ Botdan foydalanish uchun avval kanalga obuna bo'ling.",
            reply_markup=join_button()
        )

# --- CHECK BUTTON ---
@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):
    if is_subscribed(call.from_user.id):
        bot.edit_message_text(
            "✅ Obuna tasdiqlandi!\n🎬 Endi kino kodini yuboring.",
            call.message.chat.id,
            call.message.message_id
        )
    else:
        bot.answer_callback_query(call.id, "❌ Siz hali obuna bo‘lmagansiz!", show_alert=True)

# --- KINO KOD ---
@bot.message_handler(content_types=['text'])
def movie(message):
    user_id = message.from_user.id
    code = message.text.strip()

    # Agar obuna bo'lmasa, kino yubormaydi
    if not is_subscribed(user_id):
        bot.send_message(
            message.chat.id,
            "❌ Obuna bo'lmaganingiz uchun kino topilmadi. Avval kanalga obuna bo'ling:",
            reply_markup=join_button()
        )
        return

    # KINO BOR BO'LSA
    if code in MOVIES:
        bot.send_message(message.chat.id, f"🎬 '{code}' kodli kino qismlari yuborilmoqda...")
        for post_id in MOVIES[code]:
            try:
                bot.copy_message(message.chat.id, CHANNEL_ID, post_id)
                time.sleep(0.5)
            except:
                continue
    else:
        bot.send_message(message.chat.id, "❌ Bunday kodli kino topilmadi.")

print("Bot ishlayapti...")
bot.infinity_polling()

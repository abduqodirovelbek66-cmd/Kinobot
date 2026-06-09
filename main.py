import telebot
from telebot import types
import time

# ⚠️ Sozlamalar
TOKEN = "8650658473:AAEZ_A0VjLfxeRVELet0Q87ztZkOmr4Acfg"
CHANNEL_ID =-1003511706384
CHANNEL_LINK = "https://t.me/clipzXorg"

bot = telebot.TeleBot(TOKEN)

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def get_sub_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Kanalga o‘tish 📢", url=CHANNEL_LINK))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Kino kodini yuboring (masalan: 1, 11).")

@bot.message_handler(content_types=['text'])
def send_video(message):
    # 1. Obunani tekshirish
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Botdan foydalanish uchun kanalimizga obuna bo‘ling!", reply_markup=get_sub_markup())
        return

    kod = message.text.strip()
    bot.reply_to(message, f"🔍 '{kod}' kodli kinoni qidirmoqdaman, kuting...")

    # 2. Kanalni qidirish (Bu qismda kanal katta bo'lsa, xatolik berishi mumkin)
    # Eslatma: Bot kanalga admin bo'lishi shart!
    found = False
    
    # Kanal tarixini olish
    # (Diqqat: get_chat_history har doim ham kanal tarixini to'liq bermaydi, 
    # shuning uchun bazadan foydalanish tavsiya etiladi)
    try:
        # Kanal tarixini tekshirish (oxirgi 100 ta xabar)
        messages = bot.get_chat_history(CHANNEL_ID, limit=100)
        
        # Kodni o'z ichiga olgan xabarlarni yig'ish
        parts = []
        for msg in messages:
            if msg.caption and kod in msg.caption:
                parts.append(msg)
        
        # Xabarlarni xabar ID'si bo'yicha tartiblash (ketma-ket chiqishi uchun)
        parts.sort(key=lambda x: x.message_id)

        if parts:
            for part in parts:
                bot.copy_message(message.chat.id, CHANNEL_ID, part.message_id)
                time.sleep(0.5)
            found = True
        else:
            bot.send_message(message.chat.id, "❌ Bunday kodli kino topilmadi.")
            
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xatolik yuz berdi: {e}")

print("Bot ishga tushdi...")
bot.infinity_polling()

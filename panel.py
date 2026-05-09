import telebot
from telebot import types
import cv2
import pyautogui
import os
import ctypes

# Твой токен и ID (чтобы только ты мог управлять)
API_TOKEN = 'ТВОЙ_ТОКЕН_БОТА'
ADMIN_ID = ТВОЙ_ID_ЦИФРАМИ  # Узнай свой ID в @getmyid_bot

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'panel'])
def send_welcome(message):
    if message.from_user.id == ADMIN_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("📸 Камера")
        btn2 = types.KeyboardButton("🖥 Скриншот")
        btn3 = types.KeyboardButton("🔒 Блок ПК")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, "🛠 <b>Управление HOME-PC_inyx</b>", parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if message.from_user.id == ADMIN_ID:
        if message.text == "📸 Камера":
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite("cam.png", frame)
                with open("cam.png", "rb") as photo:
                    bot.send_photo(message.chat.id, photo)
                os.remove("cam.png")
            cap.release()

        elif message.text == "🖥 Скриншот":
            img = pyautogui.screenshot()
            img.save("screen.png")
            with open("screen.png", "rb") as photo:
                bot.send_photo(message.chat.id, photo)
            os.remove("screen.png")

        elif message.text == "🔒 Блок ПК":
            bot.send_message(message.chat.id, "⛔ ПК заблокирован")
            ctypes.windll.user32.LockWorkStation()

bot.polling(none_stop=True)

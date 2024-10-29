import telebot 
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot("7264778097:AAEe7tNcFpIjgkeuLfknAQrWNSe4QEDe3Sg")


@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_help = KeyboardButton('Чем могу помочь?')
    markup.add(button_help)
    bot.send_message(message.chat.id, 'Привет! Нажми кнопку "Чем могу помочь?".', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Чем могу помочь?')
def send_help_options(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_option1 = KeyboardButton('Опция 1')
    button_option2 = KeyboardButton('Опция 2')
    button_option3 = KeyboardButton('Опция 3')
    button_back = KeyboardButton('Вернуться в меню')
    markup.add(button_option1, button_option2, button_option3, button_back)
    bot.send_message(message.chat.id, 'Выбери один из вариантов:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Вернуться в меню')
def go_back_to_menu(message):
    start(message)

bot.polling(none_stop=True)
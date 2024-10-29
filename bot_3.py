import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import numpy as np
import matplotlib.pyplot as plt
import io
import json

bot = telebot.TeleBot("7264778097:AAEe7tNcFpIjgkeuLfknAQrWNSe4QEDe3Sg")

# Функция для загрузки статистики
def load_stats():
    try:
        with open('stats.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'Отлично': 0, 'Нормально': 0, 'Нужно улучшить': 0}

# Функция для сохранения статистики
def save_stats(stats):
    with open('stats.json', 'w') as f:
        json.dump(stats, f)

# Функция для загрузки предложений
def load_suggestions():
    try:
        with open('suggestions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Функция для сохранения предложений
def save_suggestions(suggestions):
    with open('suggestions.json', 'w') as f:
        json.dump(suggestions, f)

stats = load_stats()
suggestions = load_suggestions()

# Приветствие и описание функций
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_f_to_w = KeyboardButton('Частота в длину волны')
    button_e_to_w = KeyboardButton('Энергия в длину волны')
    button_w_to_f = KeyboardButton('Длина волны в частоту')
    button_w_to_e = KeyboardButton('Длина волны в энергию')
    button_analyze_spectrum = KeyboardButton('Анализ спектра')
    button_calculate_fluence = KeyboardButton('Вычислить флюенс')
    button_survey = KeyboardButton('Опрос')
    markup.add(button_f_to_w, button_e_to_w, button_w_to_f, button_w_to_e, button_analyze_spectrum, button_calculate_fluence, button_survey)
    bot.send_message(message.chat.id, 'Привет! Я бот, который может:\n1. Переводить частоту излучения или энергию фотона в длину волны и обратно.\n2. Вычислять длину волны в энергию и частоту.\n3. Анализировать спектры.\n4. Вычислять флюенс лазерной системы.\n5. Проводить опросы.', reply_markup=markup)

# Перевод частоты излучения в длину волны
@bot.message_handler(func=lambda message: message.text == 'Частота в длину волны')
def frequency_to_wavelength(message):
    bot.send_message(message.chat.id, 'Введите частоту в Гц:')
    bot.register_next_step_handler(message, convert_frequency)

def convert_frequency(message):
    try:
        frequency = float(message.text)
        c = 3e8  # Скорость света в вакууме, м/с
        wavelength = c / frequency
        bot.send_message(message.chat.id, f'Длина волны: {wavelength:.2e} м')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное числовое значение частоты.')

# Перевод энергии фотона в длину волны
@bot.message_handler(func=lambda message: message.text == 'Энергия в длину волны')
def energy_to_wavelength(message):
    bot.send_message(message.chat.id, 'Введите энергию в Дж:')
    bot.register_next_step_handler(message, convert_energy)

def convert_energy(message):
    try:
        energy = float(message.text)
        h = 6.626e-34  # Постоянная Планка, Дж·с
        c = 3e8  # Скорость света в вакууме, м/с
        wavelength = h * c / energy
        bot.send_message(message.chat.id, f'Длина волны: {wavelength:.2e} м')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное числовое значение энергии.')

# Перевод длины волны в частоту
@bot.message_handler(func=lambda message: message.text == 'Длина волны в частоту')
def wavelength_to_frequency(message):
    bot.send_message(message.chat.id, 'Введите длину волны в метрах:')
    bot.register_next_step_handler(message, convert_wavelength_to_frequency)

def convert_wavelength_to_frequency(message):
    try:
        wavelength = float(message.text)
        c = 3e8  # Скорость света в вакууме, м/с
        frequency = c / wavelength
        bot.send_message(message.chat.id, f'Частота: {frequency:.2e} Гц')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное числовое значение длины волны.')

# Перевод длины волны в энергию
@bot.message_handler(func=lambda message: message.text == 'Длина волны в энергию')
def wavelength_to_energy(message):
    bot.send_message(message.chat.id, 'Введите длину волны в метрах:')
    bot.register_next_step_handler(message, convert_wavelength_to_energy)

def convert_wavelength_to_energy(message):
    try:
        wavelength = float(message.text)
        h = 6.626e-34  # Постоянная Планка, Дж·с
        c = 3e8  # Скорость света в вакууме, м/с
        energy = h * c / wavelength
        bot.send_message(message.chat.id, f'Энергия: {energy:.2e} Дж')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное числовое значение длины волны.')

# Вычисление положения резонанса и ширины на полувысоте
@bot.message_handler(func=lambda message: message.text == 'Анализ спектра')
def analyze_spectrum(message):
    bot.send_message(message.chat.id, 'Пожалуйста, загрузите файл спектра в формате .txt:')
    bot.register_next_step_handler(message, process_spectrum_file)

def process_spectrum_file(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Преобразование байтового файла в текстовый формат
        spectrum_data = np.loadtxt(io.StringIO(downloaded_file.decode('utf-8')), delimiter=' ')
        wavelengths, intensities = spectrum_data[:, 0], spectrum_data[:, 1]

        peak_index = np.argmax(intensities)
        peak_wavelength = wavelengths[peak_index]
        half_max = intensities[peak_index] / 2
        half_max_indices = np.where(intensities >= half_max)[0]
        fwhm = wavelengths[half_max_indices[-1]] - wavelengths[half_max_indices[0]]
        
        plt.plot(wavelengths, intensities)
        plt.axvline(x=peak_wavelength, color='r', linestyle='--', label=f'Пик: {peak_wavelength:.2f} м')
        plt.axhline(y=half_max, color='g', linestyle='--', label=f'Ширина на полувысоте: {fwhm:.2f} м')
        plt.legend()
        plt.xlabel('Длина волны (м)')
        plt.ylabel('Интенсивность')
        plt.title('Спектр')
        plt.savefig('spectrum_analysis.png')
        
        bot.send_photo(message.chat.id, open('spectrum_analysis.png', 'rb'))
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {str(e)}')

# Вычисление флюенса лазерной системы по средней мощности
@bot.message_handler(func=lambda message: message.text == 'Вычислить флюенс')
def calculate_fluence(message):
    bot.send_message(message.chat.id, 'Введите среднюю мощность лазера в ваттах:')
    bot.register_next_step_handler(message, get_average_power)

def get_average_power(message):
    try:
        average_power = float(message.text)
        bot.send_message(message.chat.id, 'Введите длительность импульса в наносекундах:')
        bot.register_next_step_handler(message, get_pulse_duration, average_power)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное числовое значение средней мощности.')

def get_pulse_duration(message, average_power):
    try:
        pulse_duration = float(message.text) * 1e-9  # Конвертация из наносекунд в секунды
        fluence = average_power * pulse_duration
        bot.send_message(message.chat.id, f'Флюенс лазерной системы: {fluence:.2e} Дж/см²')
        show_main_menu(message)  # Возврат в главное меню после вычисления
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное числовое значение длительности импульса.')

# Опрос пользователя о его опыте использования бота
@bot.message_handler(func=lambda message: message.text == 'Опрос')
def survey(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_good = KeyboardButton('Отлично')
    button_bad = KeyboardButton('Нужно улучшить')
    button_neutral = KeyboardButton('Нормально')
    markup.add(button_good, button_neutral, button_bad)
    bot.send_message(message.chat.id, 'Как бы вы оценили свой опыт использования бота?', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Отлично', 'Нормально', 'Нужно улучшить'])
def survey_feedback(message):
    stats[message.text] += 1
    save_stats(stats)

    if message.text == 'Отлично':
        bot.send_message(message.chat.id, 'Спасибо! Рады, что вам понравилось.')
        show_main_menu(message)
    elif message.text == 'Нормально':
        bot.send_message(message.chat.id, 'Спасибо за ваш отзыв! Какие функции можно улучшить?')
        bot.register_next_step_handler(message, get_feedback)
    else:
        bot.send_message(message.chat.id, 'Спасибо за ваш отзыв! Какие функции вы хотели бы видеть?')
        bot.register_next_step_handler(message, get_feedback)

def get_feedback(message):
    feedback = message.text
    suggestions.append(feedback)
    save_suggestions(suggestions)
    bot.send_message(message.chat.id, f'Спасибо за ваши предложения: {feedback}')
    show_main_menu(message)  # Возврат в главное меню после получения обратной связи

# Функция для возврата в главное меню
def show_main_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_f_to_w = KeyboardButton('Частота в длину волны')
    button_e_to_w = KeyboardButton('Энергия в длину волны')
    button_w_to_f = KeyboardButton('Длина волны в частоту')
    button_w_to_e = KeyboardButton('Длина волны в энергию')
    button_analyze_spectrum = KeyboardButton('Анализ спектра')
    button_calculate_fluence = KeyboardButton('Вычислить флюенс')
    button_survey = KeyboardButton('Опрос')
    markup.add(button_f_to_w, button_e_to_w, button_w_to_f, button_w_to_e, button_analyze_spectrum, button_calculate_fluence, button_survey)
    bot.send_message(message.chat.id, 'Возврат в главное меню.', reply_markup=markup)

print("Bot is running...")
bot.polling()
import telebot
from telebot import types
import webbrowser
import schedule
import time
from threading import Thread
import sqlite3

bot = telebot.TeleBot('8152688165:AAG2uMcX1s_HqkDx3jaMZQuIYHrG7Ud3kV4')

# Функция для инициализации базы данных
def init_db():
    conn = sqlite3.connect('user.db')  # Создаем или открываем базу данных
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,  -- Используем INTEGER PRIMARY KEY для автоинкремента
            name TEXT
        )
    ''')  # Создаем таблицу, если она не существует
    conn.commit()
    conn.close()

# Функция для добавления пользователя в базу данных
def add_user(user_id, name):
    conn = sqlite3.connect('user.db')
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)', (user_id, name))
    conn.commit()
    conn.close()

# Функция для получения всех пользователей
def get_all_users():
    conn = sqlite3.connect('user.db')
    cur = conn.cursor()
    cur.execute('SELECT id FROM users')  # Исправлено с cur.execut на cur.execute
    users = cur.fetchall()
    conn.close()
    return [user[0] for user in users]  # Возвращаем список ID пользователей

# Функция для отправки ежедневного сообщения
def send_daily_message():
    users = get_all_users()
    for user_id in users:
        bot.send_message(user_id, 'Доброе утро! ☀️\n\n<b>Не забывай делать зарядку и разминку в течение дня! Это поможет поддерживать тело в тонусе!</b>', parse_mode='html')

# Планировщик задач, который проверяет расписание
def schedule_checker():
    while True:  # Бесконечный цикл
        schedule.run_pending()  # Выполняем запланированные задачи
        time.sleep(1)  # Ожидаем 1 секунду перед следующей проверкой

# Инициализация базы данных
init_db()

# Планируем отправку ежедневных сообщений
schedule.every().day.at('10:00').do(send_daily_message)

# Запускаем планировщик в отдельном потоке, чтобы он не мешал работе бота
Thread(target=schedule_checker).start()

@bot.message_handler(commands=['site'])  # Видеоресурс
def site(message):
    webbrowser.open('https://www.youtube.com/@mos-clinics')

@bot.message_handler(commands=['start'])
def main(message):
    user_id = message.chat.id  # Исправлено на message.chat.id
    user_name = message.from_user.first_name  # Получаем имя пользователя
    add_user(user_id, user_name)  # Добавляем пользователя в базу данных
    
    # Создаем обычные кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Шейно-грудная гимнастика')
    btn2 = types.KeyboardButton('Упражнения для позвоночника')
    btn3 = types.KeyboardButton('Снятие спазма шеи')
    btn4 = types.KeyboardButton('Разминка для шеи')
    
    # Добавляем кнопки в клавиатуру
    markup.row(btn1, btn2, btn3, btn4)

    bot.send_message(
        message.chat.id,
        f'Привет, {user_name}!\n\nВыбери упражнение:\n\n'
        '<b>Шейно-грудная гимнастика:</b> Упражнения для укрепления и снятия напряжения с мышц шеи и верхней части спины.\n\n'
        '<b>Упражнения для позвоночника:</b> Комплекс для поддержания гибкости и здоровья всего позвоночника.\n\n'
        '<b>Снятие спазма шеи:</b> Упражнения для расслабления и устранения боли в шейных мышцах.\n\n'
        '<b>Разминка для шеи:</b> Легкие движения для улучшения подвижности и разогрева мышц шеи.',
        reply_markup=markup,
        parse_mode='html'
    )

@bot.message_handler(func=lambda message: True)
def on_click(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    
    elif message.text == 'Шейно-грудная гимнастика':
        markup1 = types.InlineKeyboardMarkup()
        markup1.add(types.InlineKeyboardButton('Смотреть видеоурок', url='https://www.youtube.com/watch?v=AG38P6_MetM'))
        bot.send_message(message.chat.id, 'Вот видео гимнастики для шейно-грудного отдела:', reply_markup=markup1)
    
    elif message.text == 'Упражнения для позвоночника':
        markup2 = types.InlineKeyboardMarkup()
        markup2.add(types.InlineKeyboardButton('Смотреть видеоурок', url='https://www.youtube.com/watch?v=6WC-RScdfOI&t=1s'))
        bot.send_message(message.chat.id, 'Вот видео упражнений для позвоночника:', reply_markup=markup2)
    
    elif message.text == 'Снятие спазма шеи':
        markup3 = types.InlineKeyboardMarkup()
        markup3.add(types.InlineKeyboardButton('Смотреть видеоурок', url='https://www.youtube.com/watch?v=3rUqPLsgeDc'))
        bot.send_message(message.chat.id, 'Вот видео для снятия спазма мышц шеи:', reply_markup=markup3)

    elif message.text == 'Разминка для шеи':
        markup4 = types.InlineKeyboardMarkup()
        markup4.add(types.InlineKeyboardButton('Смотреть видеоурок', url='https://www.youtube.com/watch?v=yM4FFY0u0JY'))
        bot.send_message(message.chat.id, 'Вот видео упражнения для разминки мышц шеи:', reply_markup=markup4)

@bot.message_handler(content_types=['photo', 'audio', 'video'])  # Определение типа файла
def get_photo(message):
    bot.reply_to(message, 'Извини, я тебя не понимаю')

# Запуск бота
bot.polling(none_stop=True)

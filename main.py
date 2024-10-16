import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot('8152688165:AAG2uMcX1s_HqkDx3jaMZQuIYHrG7Ud3kV4')

@bot.message_handler(commands= ['site']) # Видеоресурс
def site(message):
    webbrowser.open('https://www.youtube.com/@mos-clinics')



@bot.message_handler(commands=['start'])
def main(message):
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
    f'Привет, {message.from_user.first_name}!\n\nВыбери упражнение:\n\n'
    '<b>Шейно-грудная гимнастика:</b> Упражнения для укрепления и снятия напряжения с мышц шеи и верхней части спины.\n\n'
    '<b>Упражнения для позвоночника:</b> Комплекс для поддержания гибкости и здоровья всего позвоночника.\n\n'
    '<b>Снятие спазма шеи:</b> Упражнения для расслабления и устранения боли в шейных мышцах.\n\n'
    '<b>Разминка для шеи:</b> Легкие движения для улучшения подвижности и разогрева мышц шеи.',
    reply_markup=markup,
    parse_mode ='html'
)


@bot.message_handler(func=lambda message: True)
def on_click(message):
    if message.text == 'Шейно-грудная гимнастика':
        # Создаем inline-клавиатуру для перехода по ссылке
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
        markup2 = types.InlineKeyboardMarkup()
        markup2.add(types.InlineKeyboardButton('Смотреть видеоурок', url='https://www.youtube.com/watch?v=yM4FFY0u0JY'))
        bot.send_message(message.chat.id, 'Вот видео упражнения для разминки мышц шеи:', reply_markup=markup2)

    

@bot.message_handler(content_types=['photo', 'audio', 'video']) # Определение типа файла
def get_photo(message):
    bot.reply_to(message, 'Извини, я тебя не понимаю')


@bot.message_handler() # Любой текст, любые данные поступающие от пользователя
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')


bot.polling(none_stop=True)
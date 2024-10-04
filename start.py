import sqlite3
from telebot import telebot, types
import gpt_requests

# Инициализация бота
bot = telebot.TeleBot("8112065151:AAFr0xxzD61Rx4f-BF_g6y3CfLaoHcXrGTE")

# Переменная для хранения состояния пользователя
user_data = {}


# Функция отправки главного меню с кнопками
def send_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    markup.add(types.KeyboardButton("Изменить данные о себе"))
    markup.add(types.KeyboardButton("Отчет по лабораторной работе"))
    markup.add(types.KeyboardButton("Отчет по практической работе"))
    markup.add(types.KeyboardButton("Отчет по производственной практике"))
    markup.add(types.KeyboardButton("Отчет по учебной практике"))
    markup.add(types.KeyboardButton("Курсовая работа"))
    markup.add(types.KeyboardButton("Отчет по преддипломной практике"))
    markup.add(types.KeyboardButton("Выпускная квалификационная работа (ВКР)"))
    markup.add(types.KeyboardButton("Отчет по научно-исследовательской работе (НИР)"))
    markup.add(types.KeyboardButton("Реферат"))
    markup.add(types.KeyboardButton("Отчет по проекту"))

    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)


# Функция для запроса учебного заведения
def request_university(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Назад"))

    bot.send_message(chat_id, "Введите название учебного заведения или нажмите 'Назад', чтобы выйти:",
                     reply_markup=markup)
    bot.register_next_step_handler(message, process_university)


def process_university(message):
    chat_id = message.chat.id
    if message.text == "Назад":
        bot.send_message(chat_id, "Вы вышли из процесса ввода данных.")
        return  # Завершение процесса, если нажата кнопка "Назад"

    user_data['university'] = message.text
    bot.send_message(chat_id, "Учебное заведение сохранено.")
    get_student_name(message)  # Переход к вводу ФИО студента


# Функция для получения информации с кнопкой "Назад"
def get_input_with_back(message, prompt, key, next_step):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Назад"))

    bot.send_message(chat_id, f"{prompt} или нажмите 'Назад', чтобы вернуться:", reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: process_input(msg, key, next_step))


# Функция для обработки ввода
def process_input(message, key, next_step):
    chat_id = message.chat.id
    if message.text == "Назад":
        handle_back_navigation(key, message)  # Обработка нажатия кнопки "Назад"
        return

    user_data[key] = message.text
    bot.send_message(chat_id, f"{key} сохранено.")
    next_step(message)


# Обработка навигации "Назад"
def handle_back_navigation(key, message):
    chat_id = message.chat.id
    if key == 'student_name':
        request_university(message)  # Возврат к вводу университета
    elif key == 'group_name':
        get_input_with_back(message, "Введите ваше ФИО", 'student_name', get_group)  # Возврат к ФИО
    elif key == 'course':
        get_input_with_back(message, "Введите вашу группу", 'group_name', get_course)  # Возврат к группе
    elif key == 'department':
        get_input_with_back(message, "Введите ваш курс", 'course', get_department)  # Возврат к курсу
    elif key == 'subject':
        get_input_with_back(message, "Введите кафедру", 'department', get_subject)  # Возврат к кафедре
    elif key == 'theme':
        get_input_with_back(message, "Введите название дисциплины", 'subject', get_theme)  # Возврат к дисциплине
    elif key == 'teacher_name':
        get_input_with_back(message, "Введите тему", 'theme', get_teacher_name)  # Возврат к теме
    elif key == 'teacher_status':
        get_input_with_back(message, "Введите ФИО преподавателя", 'teacher_name',
                            get_teacher_status)  # Возврат к ФИО преподавателя


# Функции для получения данных
def get_student_name(message):
    get_input_with_back(message, "Введите ваше ФИО", 'student_name', get_group)


def get_group(message):
    get_input_with_back(message, "Введите вашу группу", 'group_name', get_course)


def get_course(message):
    get_input_with_back(message, "Введите ваш курс", 'course', get_department)


def get_department(message):
    get_input_with_back(message, "Введите кафедру", 'department', get_subject)


def get_subject(message):
    get_input_with_back(message, "Введите название дисциплины", 'subject', get_theme)


def get_theme(message):
    get_input_with_back(message, "Введите тему", 'theme', get_teacher_name)


def get_teacher_name(message):
    get_input_with_back(message, "Введите ФИО преподавателя", 'teacher_name', get_teacher_status)


def get_teacher_status(message):
    get_input_with_back(message, "Введите статус преподавателя", 'teacher_status', final_step)


def final_step(message):
    bot.send_message(message.chat.id, "Все данные собраны. Спасибо!")
    # Здесь можно продолжать с обработкой данных и составлением отчета


# Создаем соединение с базой данных, расположенной на диске
def create_connection():
    conn = sqlite3.connect('student_data.db')  # Файл базы данных на диске
    return conn


# Проверка наличия пользователя в базе данных
def check_if_user_exists(chat_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE id=?", (chat_id,))
    user = cursor.fetchone()
    conn.close()  # Закрываем соединение после выполнения запроса
    return user is not None


# Проверка, заполнены ли все данные
def check_if_data_complete(chat_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT university, student_name, group_name, course FROM student WHERE id=?", (chat_id,))
    check_user_data = cursor.fetchone()
    conn.close()  # Закрываем соединение после выполнения запроса
    return all(check_user_data)


# Сохранение данных студента в базу данных
def save_student_data(data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO student (id, university, student_name, group_name, course) 
                      VALUES (?, ?, ?, ?, ?)''',
                   (data['chat_id'], data['university'], data['student_name'], data['group_name'], data['course']))
    conn.commit()  # Сохраняем изменения в базе данных
    conn.close()  # Закрываем соединение после сохранения


# Запрос недостающих данных
def request_missing_data(chat_id, message):
    conn = sqlite3.connect('student_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT university, student_name, group_name, course FROM student WHERE id=?", (chat_id,))
    check_user_data = cursor.fetchone()
    conn.close()

    if not check_user_data[0]:
        bot.send_message(chat_id, "Введите ваше учебное заведение:")
        bot.register_next_step_handler(message, process_university)
    elif not check_user_data[1]:
        bot.send_message(chat_id, "Введите ваше ФИО:")
        bot.register_next_step_handler(message, get_student_name)
    elif not check_user_data[2]:
        bot.send_message(chat_id, "Введите вашу группу:")
        bot.register_next_step_handler(message, get_group)
    elif not check_user_data[3]:
        bot.send_message(chat_id, "Введите ваш курс:")
        bot.register_next_step_handler(message, get_course)


# Запуск бота
if __name__ == "__main__":
    @bot.message_handler(commands=['start'])
    def start_command(message):
        chat_id = message.chat.id
        user_data['chat_id'] = chat_id

        if check_if_user_exists(chat_id):
            if check_if_data_complete(chat_id):
                send_main_menu(chat_id)  # Показываем меню выбора
            else:
                bot.send_message(chat_id, "Ваши данные неполные. Пожалуйста, введите недостающую информацию.")
                request_missing_data(chat_id, message)
        else:
            request_university(message)


    @bot.message_handler(commands=['prompt'])
    def start_command(message):
        chat_id = message.chat.id
        user_data['chat_id'] = chat_id
        gpt_requests.simple_request(message.text.replace('/prompt', ''), bot, user_data)


    bot.polling(none_stop=True)

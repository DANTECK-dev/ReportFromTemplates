from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from db import init_db, user_exists, add_user
from gpt import generate_content
from report import generate_report


async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Общение с ИИ", callback_data='chat_with_ai')],
        [InlineKeyboardButton("Генерация отчета", callback_data='generate_report')],
        [InlineKeyboardButton("Изменить данные о себе", callback_data='update_user')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)


async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'chat_with_ai':
        await query.edit_message_text("Введите ваш запрос для ИИ:")
        return

    if query.data == 'generate_report':
        user = user_exists(query.from_user.id)
        if user:
            await query.edit_message_text("Выберите тип отчета:", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Отчет по лабораторной работе", callback_data='lab_report')],
                [InlineKeyboardButton("Отчет по практической работе", callback_data='practical_report')],
                [InlineKeyboardButton("Курсовая работа", callback_data='coursework')],
                # Добавьте другие отчеты по аналогии
            ]))
        else:
            await query.edit_message_text("Пожалуйста, введите данные о себе для генерации отчета.")
            # Логика запроса данных


async def generate_report_process(update: Update, context):
    query = update.callback_query
    report_type = query.data
    prompt = f"Сгенерируй содержание для {report_type}"
    content = generate_content(prompt)

    await query.edit_message_text(
        f"Вот сгенерированное содержание для отчета:\n{content}\n\nПодтвердите, если подходит.")


if __name__ == '__main__':
    init_db()
    application = ApplicationBuilder().token('your_telegram_bot_token').build()

    start_handler = CommandHandler('start', start)
    button_handler = CallbackQueryHandler(button_handler)

    application.add_handler(start_handler)
    application.add_handler(button_handler)

    application.run_polling()

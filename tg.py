import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Токен вашего Telegram бота
API_TOKEN = ''
# ID Google таблицы, в которую будут добавляться данные
SPREADSHEET_ID = ''
# Путь к файлу json с учетными данными для доступа к Google Sheets API
GOOGLE_SHEETS_JSON = r''

# Устанавливаем соединение с Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_JSON, scope)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Получаем ID чата пользователя и сохраняем его в переменную referal_id
    referal_id = message.chat.id
    await message.reply('Пожалуйста, введите свое ФИО, email и номер телефона в одном сообщении.')


# Обработчик входящих сообщений с данными пользователя
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    # Получаем данные пользователя из сообщения
    user_data = message.text.split()
    # Если пользователь ввел недостаточно данных
    if len(user_data) < 3:
        await message.reply('Пожалуйста, введите ФИО, email и номер телефона в одном сообщении.')
        return
    # Иначе добавляем данные в Google таблицу
    sheet.append_row([message.chat.id, *user_data])
    await message.reply('Спасибо! Ваши данные успешно добавлены в Google таблицу.')


# Обработчик ошибок
async def error_handler(update, exception):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, exception)


# Регистрируем обработчик ошибок
dp.register_errors_handler(error_handler)

# Запускаем бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling())

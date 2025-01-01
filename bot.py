import asyncio
import logging
import locale
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from tasks import get_tasks_for_today, mark_task_completed, tasks

# Устанавливаем локаль для отображения дней недели на русском
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

# Токен бота
BOT_TOKEN = '7839999143:AAH6_LDAAbAyr4sWlhu70h2Up1nJxjUIeRk'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
# Список выполненных задач
completed_tasks = []

# ID чата для отправки автоматических уведомлений
CHAT_ID = None

async def send_scheduled_tasks():
    while True:
        now = datetime.now().strftime("%H:%M")
        today_tasks = get_tasks_for_today(completed_tasks)

        if today_tasks is None:
            logging.error("Функция get_tasks_for_today вернула None.")
            today_tasks = []

        tasks_to_send = [task for time, task in today_tasks if time == now]

        if tasks_to_send:
            if not CHAT_ID:
                logging.warning("CHAT_ID не установлен. Используйте /start для инициализации.")
            else:
                for task in tasks_to_send:
                    await bot.send_message(CHAT_ID, f"Напоминание: {task}")
                    logging.info(f"Отправлена задача: {task} в {now}")

        await asyncio.sleep(60)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    global CHAT_ID
    CHAT_ID = message.chat.id
    logging.info(f"CHAT_ID установлен: {CHAT_ID}")
    await message.reply(
        "Привет! Я бот для напоминаний о задачах в кофейне.\n"
        "Используй /help, чтобы узнать доступные команды."
    )

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(
        "/tasks — показать задачи на сегодня.\n"
        "/completed <task_id> — отметить задачу выполненной.\n"
        "/id — узнать ID текущего чата.\n"
        "/info — информация о боте."
    )

@dp.message_handler(commands=['tasks'])
async def tasks_command(message: types.Message):
    today_tasks = get_tasks_for_today(completed_tasks)
    if not today_tasks:
        await message.reply("На сегодня задач больше нет!")
        return

    for i, (time, task) in enumerate(today_tasks, start=1):
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Выполнить", callback_data=f"complete_{i}")
        )
        await message.reply(f"Задача {i}:\n{time} — {task}", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith('complete_'))
async def complete_task(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split('_')[1]) - 1
    today_tasks = get_tasks_for_today(completed_tasks)

    if 0 <= task_id < len(today_tasks):
        time, task = today_tasks[task_id]
        completed_tasks.append((time, task))
        await bot.answer_callback_query(callback_query.id, "✅ Задача выполнена!")
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        await bot.send_message(callback_query.message.chat.id, f"Задача выполнена: {time} — {task}")
    else:
        await bot.answer_callback_query(callback_query.id, "⚠️ Задача не найдена.")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_scheduled_tasks())
    executor.start_polling(dp, skip_updates=True)
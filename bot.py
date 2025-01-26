import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tasks import schedule_tasks, get_tasks_for_today

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Токен бота
BOT_TOKEN = '7839999143:AAH6_LDAAbAyr4sWlhu70h2Up1nJxjUIeRk'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

CHAT_ID = None  # ID чата пользователя


# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    global CHAT_ID
    CHAT_ID = message.chat.id
    await message.answer(
        "Привет! Я бот для напоминаний. Используй /tasks, чтобы увидеть задачи на сегодня."
    )
    # Запланируем задачи при запуске
    schedule_tasks(scheduler, bot, CHAT_ID)
    scheduler.start()

# Команда /tasks
@dp.message(Command("tasks"))
async def tasks_command(message: types.Message):
    tasks = get_tasks_for_today()
    if not tasks:
        await message.answer("Задач, соответствующих времени, нет!")
        return

    for i, task in enumerate(tasks):
        status = "✅ Выполнено" if task["is_completed"] else "🔄 Не выполнено"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=status, callback_data=f"complete_{i}")]
            ]
        )
        await message.answer(f"🕒 {task['time']} — {task['task']}", reply_markup=keyboard)


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "*Привет! Я бот для управления задачами и напоминаний. Вот что я умею:*\n\n"
        "📋 **Доступные команды:**\n"
        "• `/start` - Начать работу с ботом. Сохраняет ваш чат для отправки уведомлений.\n"
        "• `/help` - Узнать, как пользоваться ботом и получить помощь.\n"
        "• `/tasks` - Показать список задач на сегодня. Вы увидите список задач с кнопками для их выполнения.\n"
        "\n"
        "⏰ **Как это работает:**\n"
        "1. Задачи на каждый день и неделю уже запрограммированы.\n"
        "2. Вы будете получать напоминания о задачах в назначенное время.\n"
        "3. Вы можете видеть текущие задачи через команду `/tasks` и отмечать их как выполненные.\n"
        "\n"
        "🔄 **Как отметить задачу выполненной:**\n"
        "• Нажмите на кнопку «🔄 Не выполнено» рядом с задачей, и она будет отмечена как «✅ Выполнено».\n"
        "\n"
        "💡 **Пример использования:**\n"
        "• Введите `/tasks`, чтобы увидеть список задач.\n"
        "• Бот покажет вам задачи на сегодня и статус их выполнения.\n"
        "• Для каждой задачи будет кнопка для её выполнения.\n\n",
        parse_mode="Markdown"
    )

# Обработка нажатий на кнопки
@dp.callback_query(lambda c: c.data.startswith("complete_"))
async def complete_task(callback_query: CallbackQuery):
    task_id = int(callback_query.data.split("_")[1])
    tasks = get_tasks_for_today()

    if 0 <= task_id < len(tasks):
        task = tasks[task_id]
        if not task["is_completed"]:
            task["is_completed"] = True
            new_text = f"🕒 {task['time']} — {task['task']} ✅ Выполнено"
            await callback_query.message.edit_text(new_text)
            await callback_query.answer("Задача отмечена как выполненная!")
        else:
            await callback_query.answer("Задача уже была выполнена.")
    else:
        await callback_query.answer("Задача не найдена.", show_alert=True)

# Основная функция
async def main():
    if CHAT_ID is None:
        print("CHAT_ID не установлен. Запустите команду /start.")
    else:
        schedule_tasks(scheduler, bot, CHAT_ID)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
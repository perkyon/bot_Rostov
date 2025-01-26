import logging
import datetime
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

tasks = {
    "daily": [
        {"time": "08:00", "task": "Включить музыку на улице", "is_completed": False},
        {"time": "08:00", "task": "Фото витрины", "is_completed": False},
        {"time": "11:00", "task": "Фото витрины", "is_completed": False},
        {"time": "15:00", "task": "Фото витрины", "is_completed": False},
        {"time": "19:00", "task": "Фото витрины", "is_completed": False},
        {"time": "21:00", "task": "Фото витрины", "is_completed": False},
        {"time": "18:00", "task": "Включить проектор и гирлянду", "is_completed": False},
        {"time": "18:30", "task": "Составить список на заказ на завтра", "is_completed": False}
    ],
    "weekly": {
        "mon": [
            {"time": "12:30", "task": "Чистка кружек изнутри (замочить белые кружки средством и оттереть изнутри от налета и пятен)", "is_completed": False},
            {"time": "12:30", "task": "Замачивание маленьких питчеров кафизой", "is_completed": False},
            {"time": "12:30", "task": "Протереть зону винила, лимонадов, продукции и батончиков, протереть лампы по залу и все предметы интерьера", "is_completed": False},
            {"time": "17:30", "task": "Чистка кружек изнутри (замочить белые кружки средством и оттереть изнутри от налета и пятен)", "is_completed": False},
            {"time": "17:30", "task": "Замачивание маленьких питчеров кафизой", "is_completed": False},
            {"time": "17:30", "task": "Протереть зону винила, лимонадов, продукции и батончиков, протереть лампы по залу и все предметы интерьера", "is_completed": False}
        ],
        "tue": [
            {"time": "12:30", "task": "Чистка молок", "is_completed": False},
            {"time": "12:30", "task": "Помыть все холодильники изнутри", "is_completed": False},
            {"time": "17:30", "task": "Чистка молок", "is_completed": False},
            {"time": "17:30", "task": "Помыть все холодильники изнутри", "is_completed": False}
        ],
        "wed": [
            {"time": "12:30", "task": "Чистка духовки", "is_completed": False},
            {"time": "12:30", "task": "Замачивание и чистка блендера кафизой", "is_completed": False},
            {"time": "12:30", "task": "Замачивание чайников", "is_completed": False},
            {"time": "17:30", "task": "Чистка духовки", "is_completed": False},
            {"time": "17:30", "task": "Замачивание и чистка блендера кафизой", "is_completed": False},
            {"time": "12:32", "task": "Замачивание чайников", "is_completed": False}
        ],
        "thu": [
            {"time": "12:30", "task": "Протереть зону винила, лимонадов, продукции и батончиков, протереть лампы по залу и все предметы интерьера", "is_completed": False},
            {"time": "12:30", "task": "Почистить морозилку, поменять все бумажки внутри", "is_completed": False},
            {"time": "17:30", "task": "Протереть зону винила, лимонадов, продукции и батончиков, протереть лампы по залу и все предметы интерьера", "is_completed": False},
            {"time": "17:30", "task": "Протереть за зоной фуд помыть подставку для фруктов, выдвинуть холодильники на баре, помыть полы под ними", "is_completed": False}
        ],
        "fri": [
            {"time": "12:30", "task": "Чистка гейзеров", "is_completed": False},
            {"time": "12:30", "task": "Протереть все основы и сиропы", "is_completed": False},
            {"time": "12:30", "task": "Разобрать витрину, помыть изнутри, помыть и протереть подложки", "is_completed": False},
            {"time": "17:30", "task": "Чистка гейзеров", "is_completed": False},
            {"time": "17:30", "task": "Протереть все основы и сиропы", "is_completed": False},
            {"time": "17:30", "task": "Разобрать витрину, помыть изнутри, помыть и протереть подложки", "is_completed": False}
        ],
        "sat": [
            {"time": "12:30", "task": "Чистка молок", "is_completed": False},
            {"time": "12:30", "task": "Уборка на складе (расставить всю продукцию по местам, подмести и помыть полы, перебрать морозилки)", "is_completed": False},
            {"time": "17:30", "task": "Чистка молок", "is_completed": False},
            {"time": "17:30", "task": "Уборка на складе (расставить всю продукцию по местам, подмести и помыть полы, перебрать морозилки)", "is_completed": False}
        ],
        "sun": [
            {"time": "12:30", "task": "Чистка гриля с антижиром", "is_completed": False},
            {"time": "12:30", "task": "Замачивание термосов кафизой", "is_completed": False},
            {"time": "17:30", "task": "Чистка гриля с антижиром", "is_completed": False},
            {"time": "17:30", "task": "Замачивание термосов кафизой", "is_completed": False}
        ]
    },
    "monthly": {
        "15": [
            {"time": "12:30", "task": "Замена фильтров", "is_completed": False}
        ],
        "30": [
            {"time": "12:30", "task": "Замена фильтров", "is_completed": False}
        ]
    }
}

_last_checked_date = None  # Переменная для хранения даты последнего обновления


def reset_task_status():
    """Сбрасываем статус выполненных задач."""
    for task_list in tasks.values():
        if isinstance(task_list, list):
            for task in task_list:
                task["is_completed"] = False


def get_tasks_for_today():
    """Получить задачи на сегодня с учетом даты и времени."""
    global _last_checked_date
    today = datetime.datetime.now().date()

    # Если день изменился, сбрасываем выполненные задачи
    if _last_checked_date != today:
        reset_task_status()
        _last_checked_date = today

    # Возвращаем список задач (на сегодня, ежедневные и другие)
    today_tasks = tasks["daily"]
    return today_tasks


def mark_task_completed(task_id):
    """Отметить задачу как выполненную."""
    today_tasks = get_tasks_for_today()
    if 0 <= task_id < len(today_tasks):
        today_tasks[task_id]["is_completed"] = True
        return today_tasks[task_id]
    return None


async def send_notification(bot, chat_id, task):
    """Функция для отправки уведомлений."""
    await bot.send_message(chat_id, f"Напоминание: {task['task']}")


def schedule_tasks(scheduler: AsyncIOScheduler, bot, chat_id):
    """Запланировать задачи через APScheduler."""
    timezone = pytz.timezone("Europe/Moscow")  # Указываем часовой пояс
    for task in tasks["daily"]:
        hour, minute = map(int, task["time"].split(":"))
        scheduler.add_job(
            send_notification,
            "cron",
            hour=hour,
            minute=minute,
            args=[bot, chat_id, task],
            timezone=timezone,
        )
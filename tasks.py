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
    for key, task_list in tasks.items():
        # Убедимся, что task_list — это список или словарь списков
        if isinstance(task_list, list):
            # Обработка списка задач
            for task in task_list:
                if isinstance(task, dict) and "is_completed" in task:
                    task["is_completed"] = False
        elif isinstance(task_list, dict):
            # Обработка вложенного словаря (например, weekly, monthly)
            for sub_task_list in task_list.values():
                if isinstance(sub_task_list, list):
                    for task in sub_task_list:
                        if isinstance(task, dict) and "is_completed" in task:
                            task["is_completed"] = False


def get_tasks_for_today():
    """Получить задачи, которые прошли и ближайшие до 15:30."""
    global _last_checked_date
    today = datetime.datetime.now()
    current_time = today.time()
    cutoff_time = datetime.time(15, 30)  # Время окончания

    if _last_checked_date != today.date():
        reset_task_status()
        _last_checked_date = today.date()

    # Список для хранения уникальных задач
    unique_tasks = []
    task_ids = set()  # Для отслеживания уникальности задач

    # Фильтрация задач
    def filter_task(task_time):
        task_time_obj = datetime.datetime.strptime(task_time, "%H:%M").time()
        return task_time_obj <= current_time or task_time_obj <= cutoff_time

    # Обработка ежедневных задач
    for task in tasks["daily"]:
        if task["task"] not in task_ids and filter_task(task["time"]):
            unique_tasks.append(task)
            task_ids.add(task["task"])

    # Обработка еженедельных задач
    day_name = today.strftime("%a").lower()[:3]
    if day_name in tasks["weekly"]:
        for task in tasks["weekly"][day_name]:
            if task["task"] not in task_ids and filter_task(task["time"]):
                unique_tasks.append(task)
                task_ids.add(task["task"])

    # Обработка ежемесячных задач
    day_of_month = str(today.day)
    if day_of_month in tasks["monthly"]:
        for task in tasks["monthly"][day_of_month]:
            if task["task"] not in task_ids and filter_task(task["time"]):
                unique_tasks.append(task)
                task_ids.add(task["task"])

    return unique_tasks


async def send_notification(bot, chat_id, task):
    """Функция для отправки уведомлений."""
    try:
        await bot.send_message(chat_id, f"Напоминание: {task['task']}")
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления для задачи {task}: {e}")

def schedule_tasks(scheduler: AsyncIOScheduler, bot, chat_id):
    """Запланировать задачи через APScheduler."""
    timezone = pytz.timezone("Europe/Moscow")  # Указываем часовой пояс
    for task in tasks["daily"]:
        try:
            hour, minute = map(int, task["time"].split(":"))
            scheduler.add_job(
                send_notification,
                "cron",
                hour=hour,
                minute=minute,
                args=[bot, chat_id, task],
                timezone=timezone,
            )
        except Exception as e:
            logging.error(f"Не удалось запланировать задачу {task}: {e}")
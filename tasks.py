from datetime import datetime

# Полный список задач
tasks = {
    "daily": [
        ("08:00", "Включить музыку на улице"),
        ("09:30", "Фото витрины"),
        ("16:30", "Фото витрины"),
        ("00:39", "Включить проектор и гирлянду"),
        ("00:52", "Составить список на заказ на завтра")
    ],
    "weekly": {
        "monday": [
            ("12:30", "Чистка кружек изнутри (замочить белые кружки средством и оттереть изнутри от налета и пятен)"),
            ("12:30", "Замачивание маленьких питчеров кафизой"),
            ("12:30", "Протереть зону винила, лимонадов, продукции и батончиков, протереть лампы по залу и все предметы интерьера"),
            ("17:30", "Чистка кружек изнутри (замочить белые кружки средством и оттереть изнутри от налета и пятен)"),
            ("17:30", "Замачивание маленьких питчеров кафизой"),
            ("17:30", "Протереть зону винила, лимонадов, продукции и батончиков, протереть лампы по залу и все предметы интерьера")
        ],
        "tuesday": [
            ("12:30", "Чистка молок"),
            ("12:30", "Помыть все холодильники изнутри"),
            ("17:30", "Чистка молок"),
            ("17:30", "Помыть все холодильники изнутри")
        ],
        "wednesday": [
            ("12:30", "Чистка духовки"),
            ("12:30", "Замачивание и чистка блендера кафизой"),
            ("12:30", "Замачивание чайников"),
            ("17:30", "Чистка духовки"),
            ("17:30", "Замачивание и чистка блендера кафизой"),
            ("23:32", "Замачивание чайников")
        ],
        "thursday": [
            ("00:53", "Протереть зону винила, лимонадов, продукции и батончиков, протереть лампы по залу и все предметы интерьера"),
            ("00:53", "Почистить морозилку, поменять все бумажки внутри"),
            ("17:30", "Протереть зону винила, лимонадов, продукции и батончиков, протереть лампы по залу и все предметы интерьера"),
            ("17:30", "Почистить морозилку, поменять все бумажки внутри")
        ],
        "friday": [
            ("12:30", "Чистка гейзеров"),
            ("12:30", "Протереть все основы и сиропы"),
            ("12:30", "Разобрать витрину, помыть изнутри, помыть и протереть подложки"),
            ("17:30", "Чистка гейзеров"),
            ("17:30", "Протереть все основы и сиропы"),
            ("17:30", "Разобрать витрину, помыть изнутри, помыть и протереть подложки")
        ],
        "saturday": [
            ("12:30", "Чистка молок"),
            ("12:30", "Уборка на складе (расставить всю продукцию по местам, подмести и помыть полы, перебрать морозилки)"),
            ("17:30", "Чистка молок"),
            ("17:30", "Уборка на складе (расставить всю продукцию по местам, подмести и помыть полы, перебрать морозилки)")
        ],
        "sunday": [
            ("12:30", "Чистка гриля с антижиром"),
            ("12:30", "Замачивание термосов кафизой"),
            ("17:30", "Чистка гриля с антижиром"),
            ("17:30", "Замачивание термосов кафизой")
        ]
    },
    "monthly": {
        "02": [
            ("00:52", "Замена фильтров")
        ],
        "30": [
            ("12:30", "Замена фильтров")
        ]
    }
}

def get_tasks_for_today(completed_tasks):
    today = datetime.now()
    day_name = today.strftime("%A").lower()
    date = str(today.day)
    current_time = today.strftime("%H:%M")

    today_tasks = []

    # Ежедневные задачи
    for time, task in tasks["daily"]:
        if (time, task) not in completed_tasks and time >= current_time:
            today_tasks.append((time, task))

    # Задачи по дням недели
    if day_name in tasks["weekly"]:
        for time, task in tasks["weekly"][day_name]:
            if (time, task) not in completed_tasks and time >= current_time:
                today_tasks.append((time, task))

    # Задачи по датам
    if date in tasks["monthly"]:
        for time, task in tasks["monthly"][date]:
            if (time, task) not in completed_tasks and time >= current_time:
                today_tasks.append((time, task))

    # Возвращаем список задач
    return today_tasks

def mark_task_completed(task_id, completed_tasks):
    today_tasks = get_tasks_for_today(completed_tasks)
    if task_id < len(today_tasks):
        completed_tasks.append(today_tasks[task_id])
        return True
    return False
"""Telegram_bot"""
import logging
import json
import os
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CallbackContext, MessageHandler, filters,
                          CommandHandler, CallbackQueryHandler)

# Токен бота та файл для збереження даних користувачів
TOKEN_BOT = "7117301152:AAGL0qI__x7M0sCcD1a1f4ofF2DCBQ8Ni7U"
JSON_FILE = "user_data.json"

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def datetime_serializer(obj):
    """Функція для серіалізації datetime в рядковий формат"""
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d')
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


def save_data_to_json(file_path, data):
    """Функція для збереження даних у JSON файлі"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, default=datetime_serializer, ensure_ascii=False, indent=4)


def load_data_from_json(file_path):
    """Функція для завантаження даних з JSON файлу"""
    try:
        logging.info(f"Attempting to load data from JSON file: {file_path}")
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
            logging.info(f"Data successfully loaded from JSON file: {file_path}")
            logging.info(f"Data loaded: {data}")
            return data
    except FileNotFoundError:
        # Якщо файл не знайдено або виникла помилка декодування JSON, повертаємо порожній словник
        logging.error(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON file: {file_path}")
        return {}


def create_user_json(user_id):
    """Створення порожнього JSON-файлу для користувача"""
    return {"costs": {}, "income": {}}


def ensure_user_data_file_exists(file_path):
    """Перевіряє, чи існує файл користувача, і створює його, якщо не існує"""
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({}, f)


# Перевірка і створення файлу користувача, якщо потрібно
ensure_user_data_file_exists(JSON_FILE)

# Завантаження даних користувачів з JSON файлу
user_data = load_data_from_json(JSON_FILE)


class Task:
    """class Task"""
    def __init__(self, amount: float, comment: str, date: datetime = None):
        self.amount = amount
        self.comment = comment
        self.date = date if date else datetime.now().strftime('%Y-%m-%d')

    def to_dict(self):
        """Повертає словник, що представляє об'єкт Task."""
        return {
            "amount": self.amount,
            "comment": self.comment,
            "date": self.date
        }


async def start(update: Update, context: CallbackContext) -> None:
    """start"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        source = update.callback_query.message
    else:
        user_id = str(update.message.from_user.id)
        source = update.message

    # user_id = str(update.message.from_user.id)
    if user_id not in user_data:
        # Створення початкових даних для нового користувача
        user_data[user_id] = create_user_json(user_id)
        # Збереження оновлених даних у JSON-файлі
        save_data_to_json(JSON_FILE, user_data)

    # Завантаження даних користувачів з JSON файлу
    logging.info('Command "start" was triggered!')

    menu_keyboard = [
        [
            InlineKeyboardButton("Add costs", callback_data='add costs'),
            InlineKeyboardButton("Add income", callback_data='add income'),
        ],
        [
            InlineKeyboardButton("List costs", callback_data='list costs'),
            InlineKeyboardButton("List income", callback_data='list income'),
        ],
        [
            InlineKeyboardButton("List all", callback_data='list'),
            InlineKeyboardButton("Clear", callback_data='clear'),
        ],
        [
            InlineKeyboardButton("Remove costs", callback_data='remove costs'),
            InlineKeyboardButton("Remove income", callback_data='remove income'),
        ],
        [
            InlineKeyboardButton("Statistics costs", callback_data='statistics costs'),
            InlineKeyboardButton("Statistics income", callback_data='statistics income'),
        ],
        [
            InlineKeyboardButton("Statistics", callback_data='statistics')
        ]
    ]
    menu_button = InlineKeyboardMarkup(menu_keyboard)

    await source.reply_text(f"Hello {update.effective_user.first_name}\n"
                            "Welcome to Finance Tracker Bot!\n"
                            "Please choose one of the options below:",
                            reply_markup=menu_button)


async def add_keyboard(update: Update, context: CallbackContext, list_flag=None) -> None:
    """Add keyboard"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
    else:
        user_id = str(update.message.from_user.id)

    income_buttons = [
        [InlineKeyboardButton(category, callback_data=f'{category}')] for category in
        user_data[user_id]["income"]
    ]
    income_buttons.append([
        InlineKeyboardButton("Enter New Category", callback_data="new_category"),
        InlineKeyboardButton("Back to main", callback_data='back')
    ])

    income_keyboard = InlineKeyboardMarkup(income_buttons)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Choose a category or enter a new one:",
                                   reply_markup=income_keyboard)

    context.user_data['list_flag'] = list_flag


async def add_categories(update: Update, context: CallbackContext) -> None:
    """Add categories"""
    user_id = str(update.message.from_user.id)
    # Отримання введеної категорії витрат
    category_name = " ".join(context.args)

    if category_name not in user_data[user_id]["income"]:
        user_data[user_id]["income"][category_name] = []

    # Збереження оновлених даних у JSON-файлі
    save_data_to_json(JSON_FILE, user_data)

    await add_keyboard(update, context)


# Функція для додавання витрат
async def add_costs(update: Update, context: CallbackContext) -> None:
    """Add costs """
    user_id = str(update.message.from_user.id)
    task_parts = " ".join(context.args).split("|")
    task_amount = float(task_parts[0].strip())
    task_comment = task_parts[1].strip()
    task_date = None

    if len(task_parts) > 2:
        try:
            task_date = datetime.strptime(task_parts[2].strip(), "%Y-%m-%d")
        except ValueError:
            logging.error("Invalid dateline format")
            await update.message.reply_text("Your date argument is invalid, please use %Y-%m-%d format")
            return

    task_category = context.user_data["category"]

    h_task = Task(task_amount, task_comment, task_date)
    task = h_task.to_dict()

    if task_category not in user_data[user_id]["costs"]:
        user_data[user_id]["costs"][task_category] = []
    elif not isinstance(user_data[user_id]["costs"][task_category], list):
        user_data[user_id]["costs"][task_category] = [user_data[user_id]["costs"][task_category]]

    user_data[user_id]["costs"][task_category].append(task)

    back_button = InlineKeyboardButton("Back to main", callback_data='back')
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"Task: {task['amount']} - {task['comment']} was successfully added!",
                                    reply_markup=reply_markup)
    save_data_to_json(JSON_FILE, user_data)


async def add_income(update: Update, context: CallbackContext) -> None:
    """Add income """
    user_id = str(update.message.from_user.id)
    task_parts = " ".join(context.args).split("|")
    task_amount = float(task_parts[0].strip())
    task_comment = task_parts[1].strip()
    task_date = None

    if len(task_parts) > 2:
        try:
            task_date = datetime.strptime(task_parts[2].strip(), "%Y-%m-%d")
        except ValueError:
            logging.error("Invalid dateline format")
            await update.message.reply_text("Your date argument is invalid, please use %Y-%m-%d format")
            return

    task_category = context.user_data["category"]

    h_task = Task(task_amount, task_comment, task_date)
    task = h_task.to_dict()

    if task_category not in user_data[user_id]["income"]:
        user_data[user_id]["income"][task_category] = []
    elif not isinstance(user_data[user_id]["income"][task_category], list):
        user_data[user_id]["income"][task_category] = [user_data[user_id]["income"][task_category]]

    user_data[user_id]["income"][task_category].append(task)

    back_button = InlineKeyboardButton("Back to main", callback_data='back')
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"Task: {task['amount']} - {task['comment']} was successfully added!",
                                    reply_markup=reply_markup)

    save_data_to_json(JSON_FILE, user_data)


async def select_categories(update: Update, context: CallbackContext, list_flag=None) -> None:
    """add costs keyboard"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
    else:
        user_id = str(update.message.from_user.id)

    logging.info(f"Received command /list_costs from user ID: {user_id}")  # Логування user_id

    keyboard = [
        [
            InlineKeyboardButton("Food", callback_data='food'),
            InlineKeyboardButton("Rest", callback_data='rest'),
        ],
        [
            InlineKeyboardButton("Home", callback_data='home'),
            InlineKeyboardButton("Transport", callback_data='transport'),
        ],
        [
            InlineKeyboardButton("Sport", callback_data='sport'),
            InlineKeyboardButton("Health", callback_data='health'),
        ],
        [
            InlineKeyboardButton("Education", callback_data='education'),
            InlineKeyboardButton("Other", callback_data='other'),
        ],
        [
            InlineKeyboardButton("Back to main", callback_data='back')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Select an expense category:', reply_markup=reply_markup)

    context.user_data['list_flag'] = list_flag


async def list_period_key(update: Update, context: CallbackContext, category_flag=None) -> None:
    """add costs keyboard"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
    else:
        user_id = str(update.message.from_user.id)

    logging.info(f"Received command /list_costs from user ID: {user_id}")  # Логування user_id

    filter_keyboard = [
        [
            InlineKeyboardButton("One day", callback_data='day'),
            InlineKeyboardButton("One week", callback_data='week'),
        ],
        [
            InlineKeyboardButton("One month", callback_data='month'),
            InlineKeyboardButton("One year", callback_data='year'),
        ],
        [
            InlineKeyboardButton("Back to main", callback_data='back')
        ]
    ]
    filter_button = InlineKeyboardMarkup(filter_keyboard)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Please choose one of the period:',
                                   reply_markup=filter_button)

    context.user_data['category_flag'] = category_flag


async def list_category_key(update: Update, context: CallbackContext) -> None:
    """add costs keyboard"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
    else:
        user_id = str(update.message.from_user.id)

    logging.info(f"Received command /list_costs from user ID: {user_id}")  # Логування user_id

    filter_category = [
        [
            InlineKeyboardButton("All categories", callback_data='all_categories'),
            InlineKeyboardButton("Select category", callback_data='select_category'),
        ],
        [
            InlineKeyboardButton("Back to main", callback_data='back')
        ]
    ]
    filter_category_button = InlineKeyboardMarkup(filter_category)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Please choose one of the button:',
                                   reply_markup=filter_category_button)


async def date_filter(tasks, period):
    """Filter by the period"""
    filtered_result = []
    current_date = datetime.now().date()

    if period == 'week':
        start_date = current_date - timedelta(days=current_date.weekday())
        end_date = start_date + timedelta(days=6)
    elif period == 'month':
        start_date = datetime(current_date.year, current_date.month, 1).date()
        end_date = datetime(current_date.year, current_date.month + 1, 1).date() - timedelta(days=1)
    elif period == 'year':
        start_date = datetime(current_date.year, 1, 1).date()
        end_date = datetime(current_date.year, 12, 31).date()
    elif period == 'day':
        start_date = current_date
        end_date = current_date
    else:
        return filtered_result

    for task in tasks:
        task_date = datetime.strptime(task['date'], '%Y-%m-%d').date()
        if start_date <= task_date <= end_date:
            filtered_result.append(task)

    return filtered_result


async def category_filter(update: Update, context: CallbackContext, section: str) -> None:
    """category filter"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        source = update.callback_query.message
    else:
        user_id = str(update.message.from_user.id)
        source = update.message

    category = update.callback_query.data

    if category not in user_data[user_id][section]:
        await source.reply_text(f"This category doesn't exist in the {section} section.")
        return

    context.user_data['selected_category'] = category

    # await source.reply_text("Please select a period:")
    await list_period_key(update, context)


async def period_filter(update: Update, context: CallbackContext, section: str) -> None:
    """filter by period"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        source = update.callback_query.message
    else:
        user_id = str(update.message.from_user.id)
        source = update.message

    period = update.callback_query.data
    category = context.user_data.get('selected_category')

    if not category:
        await source.reply_text("Please select a category first.")
        return

    tasks = user_data[user_id][section][category]

    if not tasks:
        await source.reply_text(f"No tasks found for category '{category}' in the {section} section.")
        return

    filtered_tasks = await date_filter(tasks, period)

    if not filtered_tasks:
        await source.reply_text(
            f"No tasks found for category '{category}' in the {section} section for the selected period.")
        return

    tasks_list = "\n".join(
        [f"{'➖' if section == 'costs' else '➕'} {task['amount']} - {task['comment']} (Date: {task['date']})" for task in
         filtered_tasks])

    back_button = InlineKeyboardButton("Back to main", callback_data='back')
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await source.reply_text(
        f"Tasks for category '{category}' in the {section} section for the selected period:\n{tasks_list}",
        reply_markup=reply_markup)


async def list_costs(update: Update, context: CallbackContext) -> None:
    """add costs keyboard"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        source = update.callback_query.message
    else:
        user_id = str(update.message.from_user.id)
        source = update.message

    context.user_data['function_to_call'] = 'list_costs'

    logging.info(f"Received command /list_costs from user ID: {user_id}")  # Логування user_id

    if not user_data.get(user_id):
        logging.info(f"No data found for user ID: {user_id}")  # Логування відсутності даних
        if source:
            await source.reply_text("You don't have any tasks")
        return

    # Логування даних для користувача
    logging.info(f"User data for user ID {user_id}: {user_data[user_id]}")

    tasks = [task for sublist in user_data[user_id]["costs"].values() for task in sublist]
    period = context.user_data.get('period', 'year')

    filtered_tasks = await date_filter(tasks, period)

    all_costs = []

    for task in filtered_tasks:
        all_costs.append(f"➖ {task['amount']} - {task['comment']} (Date: {task['date']})")

    if not filtered_tasks:
        if source:
            await source.reply_text("No tasks for this period")
        return

    result = '\n'.join([f"{i+1}. {t}" for i, t in enumerate(all_costs)])
    logging.info(f"Tasks list for user ID {user_id}: {result}")

    back_button = InlineKeyboardButton("Back to main", callback_data='back')
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if source:
        await source.reply_text(result, reply_markup=reply_markup)


async def list_income(update: Update, context: CallbackContext) -> None:
    """add costs keyboard"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        source = update.callback_query.message
    else:
        user_id = str(update.message.from_user.id)
        source = update.message

    context.user_data['function_to_call'] = 'list_income'

    logging.info(f"Received command /list_income from user ID: {user_id}")

    if not user_data.get(user_id):
        logging.info(f"No data found for user ID: {user_id}")  # Логування відсутності даних
        if source:
            await source.reply_text("You don't have any tasks")
        return

        # Логування даних для користувача
    logging.info(f"User data for user ID {user_id}: {user_data[user_id]}")

    tasks = [task for sublist in user_data[user_id]["income"].values() for task in sublist]
    period = context.user_data.get('period', 'week')

    filtered_tasks = await date_filter(tasks, period)

    all_income = []

    for task in filtered_tasks:
        all_income.append(f"➕ {task['amount']} - {task['comment']} (Date: {task['date']})")

    if not filtered_tasks:
        if source:
            await source.reply_text("No tasks for this period")
        return

    result = '\n'.join([f"{i+1}. {t}" for i, t in enumerate(all_income)])
    logging.info(f"Tasks list for user ID {user_id}: {result}")

    back_button = InlineKeyboardButton("Back to main", callback_data='back')
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if source:
        await source.reply_text(result, reply_markup=reply_markup)


async def list_all(update: Update, context: CallbackContext) -> None:
    """add costs keyboard"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        source = update.callback_query.message
    else:
        user_id = str(update.message.from_user.id)
        source = update.message

    context.user_data['function_to_call'] = 'list_all'

    logging.info(f"Received command /list from user ID: {user_id}")  # Логування user_id

    if not user_data.get(user_id):
        logging.info(f"No data found for user ID: {user_id}")  # Логування відсутності даних
        if source:
            await source.reply_text("You don't have any tasks")
        return

        # Логування даних для користувача
    logging.info(f"User data for user ID {user_id}: {user_data[user_id]}")

    tasks_income = [task for sublist in user_data[user_id]["income"].values() for task in sublist]
    period = context.user_data.get('period', 'week')

    filtered_tasks_income = await date_filter(tasks_income, period)

    tasks_costs = [task for sublist in user_data[user_id]["costs"].values() for task in sublist]
    filtered_tasks_costs = await date_filter(tasks_costs, period)

    all_list = []

    for task in filtered_tasks_income:
        all_list.append(f"➕ {task['amount']} - {task['comment']} (Date: {task['date']})")

    for task in filtered_tasks_costs:
        all_list.append(f"➖ {task['amount']} - {task['comment']} (Date: {task['date']})")

    if len(all_list) == 0:
        if source:
            await source.reply_text("No tasks for this period")
        return

    result = '\n'.join(all_list)
    logging.info(f"Tasks list for user ID {user_id}: {result}")
    back_button = InlineKeyboardButton("Back to main", callback_data='back')
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if source:
        await source.reply_text(result, reply_markup=reply_markup)


async def remove_costs(update: Update, context: CallbackContext) -> None:
    """remove costs"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        source = update.callback_query.message
    else:
        user_id = str(update.message.from_user.id)
        source = update.message

    logging.info(f"Received command /remove_costs from user ID: {user_id}")  # Логування user_id

    if not user_data.get(user_id):
        logging.info(f"No data found for user ID: {user_id}")  # Логування відсутності даних
        if source:
            await source.reply_text("You don't have any tasks")
        return

    # Логування даних для користувача
    logging.info(f"User data for user ID {user_id}: {user_data[user_id]}")

    tasks = [task for sublist in user_data[user_id]["costs"].values() for task in sublist]
    result = '\n'.join([f"{i + 1}. {t['amount']} - {t['comment']}" for i, t in enumerate(tasks)])
    if source:
        await source.reply_text(result)

    await source.reply_text("Enter the number of the task you want to remove:")


async def remove_income(update: Update, context: CallbackContext) -> None:
    """remove income"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        source = update.callback_query.message
    else:
        user_id = str(update.message.from_user.id)
        source = update.message

    logging.info(f"Received command /remove_income from user ID: {user_id}")  # Логування user_id

    if not user_data.get(user_id):
        logging.info(f"No data found for user ID: {user_id}")  # Логування відсутності даних
        if source:
            await source.reply_text("You don't have any tasks")
        return

    # Логування даних для користувача
    logging.info(f"User data for user ID {user_id}: {user_data[user_id]}")

    context.user_data['helper'] = 'helper'

    tasks = [task for sublist in user_data[user_id]["income"].values() for task in sublist]
    result = '\n'.join([f"{i + 1}. {t['amount']} - {t['comment']}" for i, t in enumerate(tasks)])

    if source:
        await source.reply_text(result)

    await source.reply_text("Enter the number of the task you want to remove:")


async def keyboard_verification(update: Update, context: CallbackContext) -> None:
    """keyboard_verification"""
    number_text = update.message.text
    print(number_text)
    context.user_data['number_text'] = int(number_text)

    if 'helper' in context.user_data and context.user_data['helper'] == 'helper':
        key_verification = [
            [
                InlineKeyboardButton("Yes", callback_data='yes_income'),
                InlineKeyboardButton("No", callback_data='no'),
            ]
        ]
    else:
        key_verification = [
            [
                InlineKeyboardButton("Yes", callback_data='yes_costs'),
                InlineKeyboardButton("No", callback_data='no'),
            ]
        ]

    reply_markup = InlineKeyboardMarkup(key_verification)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Are you sure you want to delete this task:', reply_markup=reply_markup)


async def del_task(update: Update, context: CallbackContext, section: str) -> None:
    """delete costs"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        source = update.callback_query.message
    else:
        user_id = str(update.message.from_user.id)
        source = update.message

    task_number = context.user_data.get('number_text')
    print("Task number string:", task_number)
    if not task_number:
        await source.reply_text("Invalid task number provided.")
        return

    tasks = [task for sublist in user_data[user_id][section].values() for task in sublist]

    if task_number < 1 or task_number > len(tasks):
        await source.reply_text("You entered an invalid index")
        return

    removed_idx = task_number - 1
    removed_task = tasks.pop(removed_idx)

    for category, category_tasks in user_data[user_id][section].items():
        if removed_task in category_tasks:
            category_tasks.remove(removed_task)
            break

    await source.reply_text(f"Task {task_number} was successfully removed!")

    save_data_to_json(JSON_FILE, user_data)

    result = '\n'.join([f"{i + 1}. {t['amount']} - {t['comment']}" for i, t in enumerate(tasks)])

    back_button = InlineKeyboardButton("Back to main", callback_data='back')
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if source:
        if result:
            await source.reply_text(result, reply_markup=reply_markup)
        else:
            await source.reply_text("There are no messages in this section.")


async def clear(update: Update, context: CallbackContext) -> None:
    """add costs keyboard"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        source = update.callback_query.message
    else:
        user_id = str(update.message.from_user.id)
        source = update.message
    user_data[user_id] = {"costs": [], "income": []}

    back_button = InlineKeyboardButton("Back to main", callback_data='back')
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await source.reply_text("Cleared successfully", reply_markup=reply_markup)

    save_data_to_json(JSON_FILE, user_data)


async def static_costs(update: Update, context: CallbackContext) -> None:
    """add costs keyboard"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        source = update.callback_query.message
    else:
        user_id = str(update.message.from_user.id)
        source = update.message

    context.user_data['function_static'] = 'stat_costs'

    logging.info(f"Received command /list_costs from user ID: {user_id}")  # Логування user_id

    if not user_data.get(user_id):
        logging.info(f"No data found for user ID: {user_id}")  # Логування відсутності даних
        if source:
            await source.reply_text("You don't have any tasks")
        return

    # Логування даних для користувача
    logging.info(f"User data for user ID {user_id}: {user_data[user_id]}")

    tasks = [task for sublist in user_data[user_id]["costs"].values() for task in sublist]
    period = context.user_data.get('period', 'year')

    filtered_tasks = await date_filter(tasks, period)

    total_amount = 0

    for task in filtered_tasks:
        total_amount += task['amount']

    if not filtered_tasks:
        if source:
            await source.reply_text("No tasks for this period")
        return

    back_button = InlineKeyboardButton("Back to main", callback_data='back')
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if source:
        await source.reply_text(f"Spent this {period}: {total_amount}", reply_markup=reply_markup)


async def static_income(update: Update, context: CallbackContext) -> None:
    """static_income"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        source = update.callback_query.message
    else:
        user_id = str(update.message.from_user.id)
        source = update.message

    context.user_data['function_static'] = 'stat_income'

    logging.info(f"Received command /static_income from user ID: {user_id}")  # Логування user_id

    if not user_data.get(user_id):
        logging.info(f"No data found for user ID: {user_id}")  # Логування відсутності даних
        if source:
            await source.reply_text("You don't have any tasks")
        return

    # Логування даних для користувача
    logging.info(f"User data for user ID {user_id}: {user_data[user_id]}")

    tasks = [task for sublist in user_data[user_id]["income"].values() for task in sublist]
    period = context.user_data.get('period', 'year')

    filtered_tasks = await date_filter(tasks, period)

    total_amount = 0

    for task in filtered_tasks:
        total_amount += task['amount']

    if not filtered_tasks:
        if source:
            await source.reply_text("No tasks for this period")
        return

    back_button = InlineKeyboardButton("Back to main", callback_data='back')
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if source:
        await source.reply_text(f"Income for this {period}: {total_amount}", reply_markup=reply_markup)


async def statistics(update: Update, context: CallbackContext) -> None:
    """statistics"""
    if update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        source = update.callback_query.message
    else:
        user_id = str(update.message.from_user.id)
        source = update.message

    context.user_data['function_static'] = 'stat_all'

    logging.info(f"Received command /static from user ID: {user_id}")  # Логування user_id

    if not user_data.get(user_id):
        logging.info(f"No data found for user ID: {user_id}")  # Логування відсутності даних
        if source:
            await source.reply_text("You don't have any tasks")
        return

    # Логування даних для користувача
    logging.info(f"User data for user ID {user_id}: {user_data[user_id]}")

    tasks_income = [task for sublist in user_data[user_id]["income"].values() for task in sublist]
    tasks_costs = [task for sublist in user_data[user_id]["costs"].values() for task in sublist]
    period = context.user_data.get('period', 'year')

    filtered_tasks_income = await date_filter(tasks_income, period)
    filtered_tasks_costs = await date_filter(tasks_costs, period)

    total_income = 0
    total_costs = 0

    for task in filtered_tasks_income:
        total_income += task['amount']

    for task in filtered_tasks_costs:
        total_costs += task['amount']

    if not filtered_tasks_income and not filtered_tasks_costs:
        if source:
            await source.reply_text("No tasks for this period")
        return

    back_button = InlineKeyboardButton("Back to main", callback_data='back')
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    t_income = int(total_income)
    t_costs = int(total_costs)

    if source:
        if t_income > t_costs:
            result = t_income - t_costs
            await source.reply_text(f"Income for this {period}: {total_income}\n"
                                    f"Costs for this {period}: {total_costs}\n"
                                    f"Income {result} more then costs", reply_markup=reply_markup)
        elif t_income < t_costs:
            result = total_costs - total_income
            await source.reply_text(f"Income for this {period}: {total_income}\n"
                                    f"Costs for this {period}: {total_costs}\n"
                                    f"Costs {result} more then income", reply_markup=reply_markup)
        elif t_income == t_costs:
            await source.reply_text(f"Income for this {period}: {total_income}\n"
                                    f"Costs for this {period}: {total_costs}\n"
                                    f"Income and expenses are the same", reply_markup=reply_markup)


async def button(update, context):
    """Обробка натискання на кнопки."""
    query = update.callback_query
    callback_data = query.data
    await query.answer()

    # Відправка повідомлення користувачу
    if callback_data == 'add costs':
        await select_categories(update, context)

    elif callback_data == 'add income':
        await add_keyboard(update, context)

    elif callback_data == 'list costs':
        context.user_data['function_to_call'] = 'list_costs'
        await list_category_key(update, context)

    elif callback_data == 'list income':
        context.user_data['function_to_call'] = 'list_income'
        await list_category_key(update, context)

    elif callback_data == 'list':
        context.user_data['function_to_call'] = 'list_all'
        await list_period_key(update, context, 'new_flag')

    elif callback_data == 'remove costs':
        await remove_costs(update, context)

    elif callback_data == 'remove income':
        await remove_income(update, context)

    elif callback_data == 'yes_income':
        await del_task(update, context, 'income')

    elif callback_data == 'yes_costs':
        await del_task(update, context, 'costs')

    elif callback_data == 'no':
        await start(update, context)

    elif callback_data == 'back':
        await start(update, context)

    elif callback_data == 'clear':
        await clear(update, context)

    elif callback_data == 'statistics costs':
        context.user_data['function_static'] = 'stat_costs'
        await list_period_key(update, context, 'stat_flag')

    elif callback_data == 'statistics income':
        context.user_data['function_static'] = 'stat_income'
        await list_period_key(update, context, 'stat_flag')

    elif callback_data == 'statistics':
        context.user_data['function_static'] = 'stat_all'
        await list_period_key(update, context, 'stat_flag')

    elif callback_data == 'new_category':
        await context.bot.send_message(chat_id=query.message.chat.id,
                                       text=f'You selected: {query.data}.\n'
                                            'Now please enter the expense in the format: '
                                            '//add_categories <name category>')

    elif callback_data == 'all_categories':
        await list_period_key(update, context, 'new_flag')

    elif callback_data == 'select_category':
        category_type = context.user_data.get('function_to_call')
        if category_type == 'list_costs':
            await select_categories(update, context, 'flag_cost')
        elif category_type == 'list_income':
            await add_keyboard(update, context, 'flag_income')

    elif (callback_data == 'day'
          or callback_data == 'week'
          or callback_data == 'month'
          or callback_data == 'year'):

        function_static = context.user_data.get('function_static')
        function_to_call = context.user_data.get('function_to_call')
        context.user_data['period'] = callback_data
        category_flag = context.user_data.get("category_flag")

        if category_flag == 'new_flag':
            if function_to_call == 'list_costs':
                await list_costs(update, context)
            elif function_to_call == 'list_income':
                await list_income(update, context)

        if category_flag == 'stat_flag':
            if function_static == "stat_costs":
                await static_costs(update, context)
            elif function_static == "stat_income":
                await static_income(update, context)
            elif function_static == "stat_all":
                await statistics(update, context)

        else:
            if function_to_call == 'list_costs':
                await period_filter(update, context, 'costs')
            elif function_to_call == 'list_income':
                await period_filter(update, context, 'income')

        if function_to_call == 'list_all':
            await list_all(update, context)
        return

    else:
        category_name = query.data
        user_id = str(query.from_user.id)
        context.user_data["category"] = category_name
        list_flag = context.user_data.get("list_flag")
        if list_flag == 'flag_cost':
            await category_filter(update, context, 'costs')

        elif list_flag == 'flag_income':
            await category_filter(update, context, 'income')

        elif category_name in user_data[user_id]["income"]:
            await context.bot.send_message(chat_id=query.message.chat.id,
                                           text=f'You selected: {query.data}.\n'
                                                'Now please enter the expense in the format: '
                                                '\\add_income <amount> | <comment> | <date (optional)>.')
        elif category_name in user_data[user_id]["costs"]:
            await context.bot.send_message(chat_id=query.message.chat.id,
                                           text=f'You selected: {query.data}.\n'
                                                'Now please enter the expense in the format: '
                                                '\\add_costs <amount> | <comment> | <date (optional)>.')

        else:
            # Додаємо категорію до відповідного списку
            if category_name in user_data[user_id]["income"]:
                user_data[user_id]["income"][category_name] = []
            elif category_name in user_data[user_id]["costs"]:
                user_data[user_id]["costs"][category_name] = []

            await context.bot.send_message(chat_id=query.message.chat.id,
                                           text=f'You selected: {query.data}.\n'
                                                'Now please enter the expense in the format: '
                                                '\\add_costs <amount> | <comment> | <date (optional)>.')

        save_data_to_json(JSON_FILE, user_data)


# Запуск бота
def run():
    """run"""
    app = ApplicationBuilder().token(TOKEN_BOT).build()
    logging.info("Application build successfully!")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_costs", add_costs))
    app.add_handler(CommandHandler("add_income", add_income))
    app.add_handler(CommandHandler("select_categories", select_categories))
    app.add_handler(CommandHandler("add_categories", add_categories))
    app.add_handler(CommandHandler("add_keyboard", add_keyboard))
    app.add_handler(CommandHandler("list_costs", list_costs))
    app.add_handler(CommandHandler("list_period_key", list_period_key))
    app.add_handler(CommandHandler("list_category_key", list_category_key))
    app.add_handler(CommandHandler("list_income", list_income))
    app.add_handler(CommandHandler("list", list_all))
    app.add_handler(CommandHandler("remove_costs", remove_costs))
    app.add_handler(CommandHandler("remove_income", remove_income))
    app.add_handler(CommandHandler("clear", clear))

    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), keyboard_verification))

    app.run_polling()


if __name__ == "__main__":
    run()

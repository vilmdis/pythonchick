import json
import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, ApplicationBuilder

token_bot = '7117301152:AAGL0qI__x7M0sCcD1a1f4ofF2DCBQ8Ni7U'

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

# Завантаження даних з JSON файлу
def load_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Збереження даних у JSON файл
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

data = load_data()

# Стартова команда
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        rf'Hi {user.mention_html()}! I can help you track your expenses and incomes. Use /help to see the available commands.',
        reply_markup=ForceReply(selective=True),
    )

# Команда допомоги
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Commands:\n/add_expense <amount> <category>\n/add_income <amount> <category>\n/view_expenses\n/view_incomes\n/delete_expense <id>\n/delete_income <id>\n/stats')

# Додавання витрат
def add_expense(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    if user_id not in data:
        data[user_id] = {"expenses": [], "incomes": []}

    try:
        amount = float(context.args[0])
        category = context.args[1]
        expense = {"id": len(data[user_id]["expenses"]) + 1, "amount": amount, "category": category}
        data[user_id]["expenses"].append(expense)
        save_data(data)
        update.message.reply_text(f'Expense added: {amount} in {category}')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add_expense <amount> <category>')

# Додавання доходів
def add_income(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    if user_id not in data:
        data[user_id] = {"expenses": [], "incomes": []}

    try:
        amount = float(context.args[0])
        category = context.args[1]
        income = {"id": len(data[user_id]["incomes"]) + 1, "amount": amount, "category": category}
        data[user_id]["incomes"].append(income)
        save_data(data)
        update.message.reply_text(f'Income added: {amount} in {category}')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add_income <amount> <category>')

# Перегляд витрат
def view_expenses(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    if user_id in data and data[user_id]["expenses"]:
        expenses = "\n".join([f"{e['id']}: {e['amount']} in {e['category']}" for e in data[user_id]["expenses"]])
        update.message.reply_text(f'Your expenses:\n{expenses}')
    else:
        update.message.reply_text('No expenses found.')

# Перегляд доходів
def view_incomes(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    if user_id in data and data[user_id]["incomes"]:
        incomes = "\n".join([f"{e['id']}: {e['amount']} in {e['category']}" for e in data[user_id]["incomes"]])
        update.message.reply_text(f'Your incomes:\n{incomes}')
    else:
        update.message.reply_text('No incomes found.')

# Видалення витрат
def delete_expense(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    if user_id in data:
        try:
            exp_id = int(context.args[0])
            data[user_id]["expenses"] = [e for e in data[user_id]["expenses"] if e['id'] != exp_id]
            save_data(data)
            update.message.reply_text(f'Expense {exp_id} deleted.')
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /delete_expense <id>')
    else:
        update.message.reply_text('No expenses found.')

# Видалення доходів
def delete_income(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    if user_id in data:
        try:
            inc_id = int(context.args[0])
            data[user_id]["incomes"] = [i for i in data[user_id]["incomes"] if i['id'] != inc_id]
            save_data(data)
            update.message.reply_text(f'Income {inc_id} deleted.')
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /delete_income <id>')
    else:
        update.message.reply_text('No incomes found.')

# Статистика витрат та доходів
def stats(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    if user_id in data:
        total_expense = sum(e['amount'] for e in data[user_id]["expenses"])
        total_income = sum(i['amount'] for i in data[user_id]["incomes"])
        update.message.reply_text(f'Total expense: {total_expense}\nTotal income: {total_income}')
    else:
        update.message.reply_text('No data found.')

# Основна функція для запуску бота
def main() -> None:

    app = ApplicationBuilder().token(token_bot).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add_expense", add_expense))
    app.add_handler(CommandHandler("add_income", add_income))
    app.add_handler(CommandHandler("view_expenses", view_expenses))
    app.add_handler(CommandHandler("view_incomes", view_incomes))
    app.add_handler(CommandHandler("delete_expense", delete_expense))
    app.add_handler(CommandHandler("delete_income", delete_income))
    app.add_handler(CommandHandler("stats", stats))

    app.run_polling()

if __name__ == '__main__':
    main()

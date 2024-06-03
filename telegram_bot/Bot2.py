import json
import logging
import os
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters, CallbackQueryHandler)

token_bot = '7117301152:AAGL0qI__x7M0sCcD1a1f4ofF2DCBQ8Ni7U'
user_data = dict()

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

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

async def start(update: Update, context: CallbackContext) -> None:
    logging.info('Command "start"" was triggered!')
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

    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}\n'
        'Welcome to my Bot!\n'
        'Please, choose an option:',
        reply_markup=menu_button
    )

async def spend(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    categorize_to_spend = {'Games': 0, 'Food': 0, 'Music': 0, 'Crypto': 0}
    if user_id not in
    if not user_data.get(user_id):
        user_data[user_id] = []

# categorize_to_income = dict()

def run():
    app = ApplicationBuilder().token(token_bot).build()
    logging.info('Application build successfully!')
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', start))
    app.add_handler(CommandHandler('categorize', categorize_list))
    # app.add_handler(CommandHandler('help', list_task))
    # app.add_handler(CommandHandler('start', remove_task))
    # app.add_handler(CommandHandler('help', clear))
    # app.add_handler(CommandHandler('start', mark_completed))
    # app.add_handler(CommandHandler('help', check_deadlines))

    app.run_polling()

if __name__ == '__main__':
    run()

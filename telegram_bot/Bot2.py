import json
import logging
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler

token_bot = '7117301152:AAGL0qI__x7M0sCcD1a1f4ofF2DCBQ8Ni7U'


logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

async def start(update: Update, context: CallbackContext) -> None:
    logging.info('Command "start"" was triggered!')
    await update.message.reply_text(
        'Welcome to my ToDo list Bot!\n'
        'Commands:\n'
        'Chose categorize to spend money: /categorize\n'
        'List tasks: /list\n'
        'Remove task: /remove <task number>\n'
        'Clear tasks: /clear\n'
    )

async def categorize(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Games\n'
        'Food\n'
        'Music\n'
        'Crypto\n'
    )

# async def categorize(update: Update, context: CallbackContext) -> None:



def run():
    app = ApplicationBuilder().token(token_bot).build()
    logging.info('Application build successfully!')
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', start))
    app.add_handler(CommandHandler('categorize', categorize))
    # app.add_handler(CommandHandler('help', list_task))
    # app.add_handler(CommandHandler('start', remove_task))
    # app.add_handler(CommandHandler('help', clear))
    # app.add_handler(CommandHandler('start', mark_completed))
    # app.add_handler(CommandHandler('help', check_deadlines))

    app.run_polling()

if __name__ == '__main__':
    run()

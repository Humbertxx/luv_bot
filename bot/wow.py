from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

import time
import requests
import random
import os
import asyncio

import cowsay

from brain import query


async def main():
    print('starting bot...')

    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('lo_quiero', files_command))
    app.add_handler(CommandHandler('por_que', por_que_command))
    app.add_handler(CommandHandler('cow', cow_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)

    await app.initialize()
    await app.start()
    await app.updater.start_polling(poll_interval=3)
    print('Polling...')

    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

# start bot 
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(' ur <3 is listening. with love')
    user_data = context.user_data
    user_data['first_name'] = update.effective_user.first_name
    await update.message.reply_text(f"Hello, {user_data['first_name']}!")
    time.sleep(3)
    await context.bot.send_video(chat_id=update.message.chat_id, video=open('images/Justin Bieber Is Working Hard So He Can Please You.mp4', 'rb'), supports_streaming=True)

# cow say
async def cow_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Moo? (Please add text)")
        return
    message = ' '.join(context.args)
    cow_art = cowsay.cowsay(message)
    # Send with Markdown to preserve ASCII alignment
    await update.message.reply_text(
        f"```\n{cow_art}\n```", 
        parse_mode=ParseMode.MARKDOWN_V2
    )
    
# what can i do command?
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('tienes: "/file", "/por_que" y "/lo_quiero", "/cow" ')


# random cat call
async def files_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    cat_key = os.getenv("CAT_API")
   
    api = f'https://api.thecatapi.com/v1/images/search?limit=10&breed_ids=beng&api_key={cat_key}'

    response = requests.get(api, timeout=10)
    response.raise_for_status()
    images = response.json()
    if not images:
        await update.message.reply_text("No pude encontrar una imagen ahora mismo.")
        return

    url = random.choice(images)['url']
    
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=url)

# call holy AI
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    response = query(text)

    print('Bot:', response)
    await update.message.reply_text(response)

# reasons to be
async def por_que_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reasons = [
        "pq es muy guapo", 
        "pq te ama mucho", 
        "pq la gente buena persona", 
        "pq no se defendió", 
        "pq no tiene la razón",
        "pq tienes que es", 
        "pq eres", 
        "pq te gustan las almendras",
        "pq de nuevo eres"
    ]
    chosen_reason = random.choice(reasons)
    await update.message.reply_text(chosen_reason)


#error handler for me to debug. stuff
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    asyncio.run(main())

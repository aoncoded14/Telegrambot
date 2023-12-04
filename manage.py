from typing import Final

from telegram import Update

from dotenv import load_dotenv

import os

from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes 

from langchain.document_loaders import TextLoader

load_dotenv()

TOKEN: Final = os.getenv('TOKEN')

BOT_USERNAME: Final = '@aonchat_bot'

DATABASE = None

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is Aon how can i be of service to you today?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What can i do to help you today?')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is  a custom command')

#Incorporating Langchain
async def load(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loader = TextLoader('/home/aonlinxed/projects/bot/state-of-the-union.txt') #Sampletext

#Responses using if statements
def handle_response(text: str) -> str:
    processed: str = text.lower() #This will convert all the text to lowercase
    
    if 'hello' in processed:
        return 'Hey there'
    
    if 'how are you' in processed:
        return 'I am doing good'
    
    if 'how can i get your product' in processed:
        return 'Please Suscribe for more information!'
    
    return 'I do not understand what you wrote... '

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type #Will inform us if it is a group chat or private chat
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    #Differentiating talking in group vs in private
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')    #Prints Program Start
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    #Check for Updates i.e Polls the bot
    print('Polling...')    #Prints Polling
    app.run_polling(poll_interval=3)

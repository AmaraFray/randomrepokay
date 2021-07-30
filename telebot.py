import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ChatMemberHandler
from bs4 import BeautifulSoup
import requests
import os


PORT = int(os.environ.get('PORT', 5000))

list_of_people = {'Idhikash':1264200196,'Shruti':1750269209,'Neha':1503912088} 

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def all(update, context):
    """Send a message when the command /help is issued."""
    message = ""
    for i in list_of_people:
      message += f'[{i}](tg://user?id={list_of_people[i]}) '
    update.message.reply_text(message,parse_mode='MarkdownV2')
    
def in_command(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user
    user_name = user.username or user.first_name or 'anonymous'
    print(user.id, user_name)
    message = f'Thanks for opting in {user_name}'
    update.message.reply_text(message)
            


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def dog(update, context):
    """Echo the user message."""
    update.message.reply_text("Everyone loves dogs!")


def wyr(update, context):
  link = requests.get('http://either.io/').text
  soup = BeautifulSoup(link, 'lxml')
  op2find = soup.find('div', class_='result result-2')
  option2 = op2find.find('span', class_='option-text').text
  op1 = soup.find('div', class_='result result-1')
  option1 = op1.find('span', class_='option-text').text
  wyr_st = "Would you rather: " + option1 + " or " + option2
  update.message.reply_text(wyr_st)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1915350419:AAGST74n3WWJ5GqlENycs_ybhdWjPDZsszc", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("all", all))
    dp.add_handler(CommandHandler("Dog", dog))
    dp.add_handler(CommandHandler("wyr", wyr))
    dp.add_handler(CommandHandler("in", in_command))

    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path="1915350419:AAGST74n3WWJ5GqlENycs_ybhdWjPDZsszc")
    updater.bot.set_webhook("https://cryptic-mesa-08995.herokuapp.com/" + "1915350419:AAGST74n3WWJ5GqlENycs_ybhdWjPDZsszc")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
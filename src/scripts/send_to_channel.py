import logging
import os

import telegram


def send_msg(msg):
    BOT_TOKEN = os.environ.get('TOKEN')
    CHANNEL_ID = os.environ.get('CHANNEL_ID')
    bot = telegram.Bot(BOT_TOKEN)
    try:
        bot.send_message(CHANNEL_ID, msg, disable_web_page_preview=True,
                         parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception as ex:
        logging.error(
            f'Exception of type {type(ex).__name__} in (): {str(ex)}')
    finally:
        logging.info('Finished sending.')

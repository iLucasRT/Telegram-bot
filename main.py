import logging
import multiprocessing

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from multiprocessing import Process
import Prices, BNA, EthGas, Alerta, Restart, repeater
from repeater import RepeatedTimer
import subprocess
import time
import random

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.

################################################ Commands ###########################################################


def start(update: Update, context: CallbackContext):
    """Sends a message with three inline buttons attached."""
    fraserandom = random.randint(0, 3)
    frases = ['Bienvenido! Que alegría volver a verte', 'Hola! Encantado de ayudarte', 'Hola! ¿En que te ayudo?', 'Hola! Soy Gasi y estoy para ayudarte 😁']
    update.message.reply_text(frases[fraserandom])
    main_menu(update, context)


def main_menu(update: Update, context: CallbackContext):
    keyboard = [['🇦🇷 Economía Argentina'],
                ['₿ Crypto']]
    message = '🔼 Entrando al menú'
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)


def argentina_menu(update: Update, context: CallbackContext):
    keyboard = [['💵 Dólar', '📉 Inflación'],
                ['🖨 Circulación monetaria'],
                ['⏮️ Volver']]
    message = '¿Que deseas consultar?'
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)


def argentina_menu_dolar(update: Update, context: CallbackContext):
    keyboard = [['💵 Dólar oficial', '💵 Dólar oficial con impuestos', '💵 Cotización dólar blue'],
                ['💵 Todas las cotizaciones'],
                ['⏮️ Volver a Economía Argentina']]
    message = '¿Que cotización deseas consultar?'
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)


def crypto_menu(update: Update, context: CallbackContext):
    keyboard = [['💲 Precio de criptomonedas'],
                ['⛽ Eth Gas'],
                ['🔔 Alerta', '🔕 Desactivar alerta'],
                ['⏮️ Volver']]
    message = 'Bien, ahora selecciona una de las opciones'
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)


def remember_menu(update: Update, context: CallbackContext):
    keyboard = [['🔕 Desactivar Alerta']]
    message = 'Introducí el precio. Recordá que solo te avisaré cuando el precio sea menor 😉'
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text(message)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def call_price(update: Update, context: CallbackContext) -> None:
    """Send a message with the price of the crypto in USD"""
    reply_markup = ReplyKeyboardRemove
    keyboard = [['bitcoin', 'ethereum', 'pvu'],
                ['cardano', 'cake'],
                ['⏮️ Volver']]
    message = 'Elija la moneda a consultar'
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)


def gas_options(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardRemove
    keyboard = [['👁️‍🗨️ Todos los precios'],
                ['🐌 Low', '⏳ Normal', '🚀 Fast', '⚡ Instant'],
                ['⏮️ Volver']]
    message = 'Seleccione uno'
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)


def unkown_message(update: Update, context: CallbackContext):
    fraserandom = random.randint(0, 3)
    messages = ['Ups! Mensaje equivocado 🙈', 'Parece que todavía no tengo esa opción 🧐', 'Por favor, utiliza el menú de abajo 👇🏻', 'Esa opción es chino básico para mí 😕']
    update.message.reply_text(messages[fraserandom])


################################################ Callers ############################################################
def price(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Prices.ethereumprice(update.message.text))


def gas(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(EthGas.gaschecker(update.message.text))


def arg_functions(update: Update, context: CallbackContext):
    update.message.reply_text('Estoy chequeando los datos, dame un momento')
    time.sleep(2)
    if update.message.text == '💵 Dólar oficial':
        update.message.reply_text(BNA.dolar_oficial('a'))
    elif update.message.text == '💵 Cotización dólar blue':
        update.message.reply_text(BNA.dolar_blue())
    elif update.message.text == '🖨 Circulación monetaria':
        update.message.reply_text(BNA.circulacion_monetaria())
    elif update.message.text == '💵 Dólar oficial con impuestos':
        update.message.reply_text(BNA.dolar_oficial('💵 Dólar oficial con impuestos'))
    elif update.message.text == '💵 Todas las cotizaciones':
        update.message.reply_text(BNA.cotizaciones())
    elif update.message.text == '📉 Inflación':
        update.message.reply_text((BNA.inflacion()))


def remember_process_starter(update: Update, context: CallbackContext):
    lista = [Process(target=main_menu(update, context)), Process(target=remember(update, context))]
    lista[0].start()
    lista[1].start()



def remember(update: Update, context: CallbackContext):
    Alerta.caller(update, update.message.text)

    rt = RepeatedTimer(5, Alerta.caller, update, update.message.text)
    lista2.append(rt)
    if update.message.text == '🔕 Desactivar alerta':
        lista2[0].stop()


################################################ Callback Receiver ##################################################

def main_handler(update, context):
    logging.info(f'update : {update}')
    msg = update.message.text
    ############### Argentina menu ################
    if msg == '🇦🇷 Economía Argentina':
        argentina_menu(update, context)
    elif msg == '💵 Dólar':
        argentina_menu_dolar(update, context)
    elif msg == '📉 Inflación':
        arg_functions(update, context)
    elif msg == '🖨 Circulación monetaria':
        arg_functions(update, context)
    elif msg == '💵 Dólar oficial' or msg == '💵 Cotización dólar blue' or msg ==  '💵 Dólar oficial con impuestos' or msg == '💵 Todas las cotizaciones':
        arg_functions(update, context)
    elif msg == '⏮️ Volver a Economía Argentina':
        argentina_menu(update, context)
    ############### Crypto Menu ###################
    elif msg == '₿ Crypto':
        crypto_menu(update, context)
    elif msg == '💲 Precio de criptomonedas':
        call_price(update, context)
    ############### Remember menu #################
    #elif msg == '🔔 Alerta':
    #    remember_process_starter(update, context)
    elif msg == '🔕 Desactivar alerta':
        remember_process_starter(update, context)
    elif msg[0] in '1234567890':
        remember_process_starter(update, context)
    ############### Gas calls #####################
    elif msg == '⛽ Eth Gas':
        gas_options(update, context)
    elif msg == '🐌 Low':
        gas(update, context)
    elif msg == '⏳ Normal':
        gas(update, context)
    elif msg == '🚀 Fast':
        gas(update, context)
    elif msg == '⚡ Instant':
        gas(update, context)
    elif msg == '👁️‍🗨️ Todos los precios':
        gas(update, context)
    ##########################################################
    elif msg == '⏮️ Volver':
        main_menu(update, context)
    else:
        price(update, context)

#def echo(update: Update, context: CallbackContext) -> None:
#    Echo the user message.
#    update.message.reply_text(update.message.text)

################################################ Bot parameters #####################################################

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    #dispatcher.add_handler(CommandHandler("price", call_price))

    # on non command i.e message - echo the message on Telegram
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.text, main_handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    lista = []
    lista2 = []
    main()

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from multiprocessing import Process
from modules import Alerta, EthGas, Prices, BNA, TokenConsultant
from classes.repeater import RepeatedTimer
import time
import random
import os
import sqlite3

PORT = int(os.environ.get('PORT', '8443'))
TOKEN = "2068821450:AAH48otmZ7kwRHNs7XEi69IZpwOcMgIKPHk"


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
    frases = ['Bienvenido! Que alegría verte', 'Hola! Encantado de ayudarte', 'Hola! ¿En que te ayudo?', 'Hola! Soy Gasi, ¿En que te ayudo? 😁']
    update.message.reply_text(frases[fraserandom])
    main_menu(update, context)

def info(update: Update, context: CallbackContext):
    update.message.reply_text("Hola 😁 Mi nombre es Gasi, soy un bot que puede consultar por tí algunos datos sobre la economía Argentina o sobre criptomonedas. \n"
                              "Mi creador es Lucas. Él es una persona genial y siempre se preocupa de que yo pueda funcionar bien además de ayudarme siempre a mejorar. \n"
                              "Al ser un bot no puedo sentir sentimientos por nadie 🤔 pero cuando mi creador me habla, algo en mi es diferente")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Veo que necesitas ayuda para que pueda ayudarte 😅 \n'
                              'Pedirme ayuda es muy simple, solo debes pulsar sobre los botones del menú desplehable que saldrá en la parte inferior de tu pantalla,'
                              'esos botones contienen todo lo que puedo hacer, y, de ser necesario que ingreses algo por texto te lo indicaré yo mismo. \n'
                              'Espero haber resuelto tus dudas 🤗')

def crypto_command(update: Update, context: CallbackContext):
    update.message.reply_text('Puede que esto te parezca demasiado, pero ¿Sabías que puedo consultar el precio de mas de 13.000 criptomondas? 😲 \n'
                              'En el menú inferior podrás observar que aparecen los símbolos de algunas criptomonedas que son consideradas las más importanes, pero si necesitas consultar otra'
                              'no te preocupes, hacerlo es muy sencillo.\n'
                              'Solo debes poner lo que se conoce como símbolo. Por ejemplo: el símbolo de Bitcoin es BTC, o el de Ethereum, ETH \n')


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
                ['🔔 Alerta (en desarrollo)', '🔕 Desactivar alerta'],
                ['⏮️ Volver']]
    message = 'Bien, ahora selecciona una de las opciones'
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)


def remember_menu(update: Update, context: CallbackContext):
    keyboard = [['🔕 Desactivar Alerta']]
    message = 'Introducí el precio. Recordá que solo te avisaré cuando el precio sea menor 😉'
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text(message)

def call_price(update: Update, context: CallbackContext) -> None:
    """Send a message with the price of the crypto in USD"""
    reply_markup = ReplyKeyboardRemove
    keyboard = [['btc', 'eth', 'rvn'],
                ['ada', 'shib', 'bnb', 'doge'],
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
def price(update: Update, context: CallbackContext, token, token_name):
    update.message.reply_text(Prices.ethereumprice(token, token_name))


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
    elif msg == '🔔 Alerta (en desarrollo)':
    #    remember_process_starter(update, context)
        update.message.reply_text("Ups! Esa función todavía está en desarrollo")
    elif msg == '🔕 Desactivar alerta':
        remember_process_starter(update, context)
    #elif msg[0] in '1234567890':
        #remember_process_starter(update, context)
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
        token = update.message.text
        token = str(token)
        token = token.lower()
        token.lower()
        token, tokenName = TokenConsultant.search(token, myCursor)
        print(token, tokenName)
        if (token != False) or (tokenName != False):
            price(update, update.message.text, token, tokenName)
        else:
            num_random = random.randint(0,5)
            frases = ["Ups! No conozco ese comando",
                    "Mi creador dice que si algo funciona bien es mejor no tocarlo, y creo que por eso no reconozco el comando que me solicitas",
                    "Me gusta ayudarte pero por ahora no puedo hacerlo con eso que me pides 😢",
                    "A mi no me preguntes, solo soy un bot",
                    "Mi creador es alguien muy bueno y siempre está ayudandome a mejorar, espero que un día incluya eso que necesitas",
                    "Lamponne el pedido es simple, hacé que Lucas desarrolle la función que este usuario me pide"]
            update.message.reply_text(frases[num_random])
    """else:
        price(update, context)"""

#def echo(update: Update, context: CallbackContext) -> None:
#    Echo the user message.
#    update.message.reply_text(update.message.text)

################################################ Bot parameters #####################################################

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler('crypto', crypto_command))
    #dispatcher.add_handler(CommandHandler("price", call_price))

    # on non command i.e message - echo the message on Telegram
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.text, main_handler))

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url=('https://lucasbotskywalker.herokuapp.com/' + TOKEN))

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    myConectionn = sqlite3.connect('ddbb/tokens', check_same_thread=False)
    myCursor = myConectionn.cursor()
    lista = []
    lista2 = []
    main()
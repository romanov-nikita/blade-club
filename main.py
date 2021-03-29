import telebot as tb
from telebot.types import ReplyKeyboardMarkup

import config
import time

token = config.TOKEN

bot = tb.TeleBot(token)


class FoodCart:
    def __init__(self, name):
        self.name = name
        self.list = []


class User:
    def __init__(self, ident):
        self.ident = ident
        self.menu = 0
        self.cartName = ''


carts = []
users = []

keyboard0 = tb.types.ReplyKeyboardMarkup(True)
keyboard0.row('/start', '/help')

keyboard1 = tb.types.ReplyKeyboardMarkup(True)
keyboard1.row('/yes', '/no', '/help')

keyboard2 = tb.types.ReplyKeyboardMarkup(True)
keyboard2.row('/add', '/delete', '/ready', '/show', '/help')

keyboard3 = tb.types.ReplyKeyboardMarkup(True)
keyboard3.row('/make_cart', '/connect_cart', '/help')


@bot.message_handler(commands=['start', 'help', 'yes', 'no', 'make_cart', 'connect_cart', 'add', 'delete', 'ready', 'show'])
def commands(message):
    user = CreateFindUser(message.chat.id)
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Привет! Я бот, который поможет Вам в походах в продуктовый. Чтобы получить '
                                          'больше информации, нажми /help. Готовы начать?', reply_markup=keyboard1)
    elif message.text == '/help':
        bot.send_message(message.chat.id, config.HELPTEXT)
        time.sleep(3)
        bot.send_message(message.chat.id, 'Продолжим?')
    elif message.text == '/yes':
        bot.send_message(message.chat.id, 'Выберите что хотите сделать.', reply_markup=keyboard3)
    elif message.text == '/no':
        bot.send_message(message.chat.id, 'Если понадоблюсь, просто нажмите /start')
    elif message.text == '/make_cart':
        bot.send_message(message.chat.id, 'Создание новой тележки. Введите название тележки.')
        user.menu = 1
    elif message.text == '/connect_cart':
        bot.send_message(message.chat.id, 'Подключение к тележке. Введите название тележки.')
        user.menu = 1
    elif message.text == '/add':
        bot.send_message(message.chat.id, 'Введите название продукта, который хотите добавить.')
        user.menu = 2
    elif message.text == '/delete':
        bot.send_message(message.chat.id, 'Введите название продукта, который хотите удалить.')
        bot.send_message(message.chat.id, PrintInfo(CreateConnectCart(user.cartName).name))
        user.menu = 3
    elif message.text == '/ready':
        cart = CreateConnectCart(user.cartName)
        bot.send_message(message.chat.id, 'Ваша тележка ' + PrintInfo(cart.name) + 'Удачных покупок!',
                         reply_markup=keyboard0)
        DeleteCart(cart.name)
    elif message.text == '/show':
        cart = CreateConnectCart(user.cartName)
        bot.send_message(message.chat.id, 'Ваша тележка ' + PrintInfo(cart.name) + 'Что дальше?',
                         reply_markup=keyboard2)


@bot.message_handler(content_types=['text'])
def data(message):
    user = CreateFindUser(message.chat.id)
    if user.menu == 1:
        user.cartName = CreateConnectCart(message.text).name.lower()
        bot.send_message(message.chat.id, 'Вы подключены к тележке ' + user.cartName + '\nЧто дальше?',
                         reply_markup=keyboard2)
    elif user.menu == 2:
        cart = CreateConnectCart(user.cartName)
        cart.list.append(message.text.lower())
        bot.send_message(message.chat.id, 'Вы положили в тележку ' + message.text + '\nЧто дальше?',
                         reply_markup=keyboard2)
    elif user.menu == 3:
        cart = CreateConnectCart(user.cartName)
        DeleteFromCart(cart, message.text.lower())
        bot.send_message(message.chat.id, 'Ваша тележка ' + PrintInfo(cart.name) + 'Что дальше?',
                         reply_markup=keyboard2)




def CreateFindUser(ident) -> object:
    check = False
    for user in users:
        if user.ident == ident:
            check = True
            us = user
    if not check:
        us = User(ident)
        users.append(us)
    return us


def CreateConnectCart(name) -> object:
    check = False
    for cart in carts:
        if cart.name == name:
            check = True
            cr = cart
    if not check:
        cr = FoodCart(name)
        carts.append(cr)
    return cr


def PrintInfo(name):
    info = ''
    for cart in carts:
        if cart.name == name:
            info = cart.name + ':\n'
            for product in cart.list:
                info += '🔘' + product + '\n'
    return info

def DeleteFromCart(FoodCart, name):
    for product in FoodCart.list:
        if product == name:
            FoodCart.list.remove(product)

def DeleteCart(name) -> object:
    for cart in carts:
        if cart.name == name:
            carts.remove(cart)


bot.polling()

while True:
    pass

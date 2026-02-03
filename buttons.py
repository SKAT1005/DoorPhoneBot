from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

channel_url = 'https://t.me/+X-gpBf-p2zgwNTg6'


def subscribe():
    markup = InlineKeyboardMarkup(row_width=1)
    channel = InlineKeyboardButton('Канал', url=channel_url)
    check = InlineKeyboardButton('Проверить подписку', callback_data='menu')
    markup.add(channel, check)
    return markup



def menu():
    markup = InlineKeyboardMarkup(row_width=1)
    doorphone = InlineKeyboardButton('Домофон', callback_data='doorphone')
    smart_doorphone = InlineKeyboardButton('Умный домофон', callback_data='smart_doorphone')
    cameras = InlineKeyboardButton('Монтаж Видеонаблюдения', callback_data='cameras')
    delivery_keys = InlineKeyboardButton('Доставка ключей', callback_data='delivery_keys')
    color_door = InlineKeyboardButton("Покраска дверей", callback_data='color_door')
    support = InlineKeyboardButton('Поддержка', callback_data='support')
    markup.add(doorphone, smart_doorphone, cameras, delivery_keys, color_door, support)
    return markup


def doorphone(type):
    markup = InlineKeyboardMarkup(row_width=1)
    install = InlineKeyboardButton('Установка', callback_data=f'{type}|install')
    repair = InlineKeyboardButton('Ремонт', callback_data=f'{type}|repair')
    markup.add(install, repair)
    menu = InlineKeyboardButton('В главное меню', callback_data='menu')
    markup.add(menu)
    return markup


def back():
    markup = InlineKeyboardMarkup(row_width=1)
    menu = InlineKeyboardButton('В главное меню', callback_data='menu')
    markup.add(menu)
    return markup


def color_door():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    reason1 = KeyboardButton('Покраска двери')
    reason2 = KeyboardButton("Сварочные работы по ремонту двери")
    markup.add(reason1, reason2)
    return markup


def skip():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    skip = KeyboardButton('Пропустить')
    markup.add(skip)
    return markup


def rating(order_id):
    markup = InlineKeyboardMarkup(row_width=1)
    star1 = InlineKeyboardButton('⭐️', callback_data=f'rating|1|{order_id}')
    star2 = InlineKeyboardButton('⭐️⭐️', callback_data=f'rating|2|{order_id}')
    star3 = InlineKeyboardButton('⭐⭐️⭐️️', callback_data=f'rating|3|{order_id}')
    star4 = InlineKeyboardButton('⭐⭐️⭐️⭐️️', callback_data=f'rating|4|{order_id}')
    star5 = InlineKeyboardButton('⭐⭐️⭐️⭐️⭐️️', callback_data=f'rating|5|{order_id}')
    markup.add(star1, star2, star3, star4, star5)
    return markup


def approve():
    markup = InlineKeyboardMarkup(row_width=1)
    menu = InlineKeyboardButton('✅Принимаю✅', callback_data='menu')
    markup.add(menu)
    return markup
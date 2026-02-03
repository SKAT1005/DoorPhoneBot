import os

import django

from const import bot
from menu import menu

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DoorPhoneBot.settings')
django.setup()

from app.models import User, Order

def reg_step_3(message, chat_id, name, address):
    if message.content_type == 'text':
        phone = message.text
        User.objects.create(
            chat_id=chat_id,
            name=name,
            address=address,
            phone=phone
        )
        menu(chat_id=chat_id)
    else:
        msg = bot.send_message(chat_id=chat_id, text='Введите ваше имя')
        bot.register_next_step_handler(msg, reg_step_3, chat_id, name, address)

def reg_step_2(message, chat_id, name):
    if message.content_type == 'text':
        address = message.text
        msg = bot.send_message(chat_id=chat_id, text='Введите ваш номер телефона')
        bot.register_next_step_handler(msg, reg_step_3, chat_id, name, address)
    else:
        msg = bot.send_message(chat_id=chat_id, text='Введите ваше имя')
        bot.register_next_step_handler(msg, reg_step_2, chat_id, name)


def reg_step_1(message, chat_id):
    if message.content_type == 'text':
        name = message.text
        msg = bot.send_message(chat_id=chat_id, text='Введите ваш адрес(Город, улица, дом, квартира)')
        bot.register_next_step_handler(msg, reg_step_2, chat_id, name)
    else:
        msg = bot.send_message(chat_id=chat_id, text='Введите ваше имя')
        bot.register_next_step_handler(msg, reg_step_1, chat_id)
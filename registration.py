import os

import django

import buttons
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
        text = 'Продолжая использовать бота, ты соглашаешься с <a href="https://docs.google.com/document/d/1ARzDxdv8pvQgUcCk9wWWHTsNqPa-4MS3v0wWnaqI18Q/edit?usp=sharing">условиями использования</a> 📜✔️'
        bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.approve(), parse_mode='HTML', disable_web_page_preview=True)
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
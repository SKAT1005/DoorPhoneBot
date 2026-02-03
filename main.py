import os

import django

from review import review_step_2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DoorPhoneBot.settings')
django.setup()

from app.models import User, Order

import telebot

import buttons
from const import bot, channel_id
from menu import menu
from registration import reg_step_1
User.objects.all().delete()
Order.objects.all().delete()

def check_subscribe(chat_id):
    chat_member = bot.get_chat_member(channel_id, chat_id).status
    if chat_member in ['member', 'creator']:
        return True
    else:
        bot.send_message(text='Для продолжения работы бота подпишитесь на канал', chat_id=chat_id,
                         reply_markup=buttons.subscribe())
        return False


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if check_subscribe(chat_id=chat_id):
        user = User.objects.filter(chat_id=chat_id).first()
        if user:
            menu(chat_id=chat_id)
        else:
            msg = bot.send_message(chat_id=chat_id, text='Как к вам обращаться?')
            bot.register_next_step_handler(msg, reg_step_1, chat_id)


def doorphone(chat_id, user, type):
    if type == 'doorphone':
        text = (
            "🔒 *Обычный домофон*\n\n"
            "Классическое и проверенное решение для безопасности подъезда. "
            "Надежная защита, простота использования и долгий срок службы.\n\n"
            "Выберите необходимое действие:"
        )
    else:
        text = (
            "🚀 *Умный домофон*\n\n"
            "Современные технологии на страже вашего спокойствия! "
            "Управление со смартфона, видеозвонки, удаленное открытие двери и интеграция в систему «умный дом».\n\n"
            "Выберите необходимое действие:"
        )
    bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.doorphone(type), parse_mode='Markdown')


def install(message, chat_id, user, type):
    if message.content_type == 'text':
        link = message.text
        Order.objects.create(user=user, is_new=True, type=type, text=link)
        text = (
            "✅ *Заявка успешно создана!*\n\n"
            "Благодарим за обращение в компанию «Велес». Ваша заявка принята в работу и передана свободному специалисту.\n\n"
            "📞 *С вами свяжутся* в ближайшее время для уточнения деталей и согласования времени.\n\n"
            "⏰ *Режим работы офиса:*\n"
            "• Пн–Пт: 9:00 – 18:00\n"
            "• Сб, Вс: выходные дни\n\n"
            "_В экстренных случаях возможен выезд мастера в нерабочее время по отдельной договоренности._"
        )
        bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.back(), parse_mode='Markdown')
    else:
        text = (
            "📝 *Оформление заявки на установку*\n\n"
            "Для начала работ нам потребуется ваше согласие.\n"
            "Пожалуйста, *отправьте ссылку* на подписанный протокол или ваше согласие на индивидуальную установку.\n\n"
            "_Это обязательный шаг для соблюдения формальностей._"
        )
        msg = bot.send_message(chat_id=chat_id,text=text, reply_markup=buttons.back(), parse_mode='Markdown')
        bot.register_next_step_handler(msg, install, chat_id, user)


def repair(message, chat_id, user, type):
    if message.content_type == 'text':
        reason = message.text
        Order.objects.create(user=user, type=type, text=reason)
        text = (
            "✅ *Заявка успешно создана!*\n\n"
            "Благодарим за обращение в компанию «Велес». Ваша заявка принята в работу и передана свободному специалисту.\n\n"
            "📞 *С вами свяжутся* в ближайшее время для уточнения деталей и согласования времени.\n\n"
            "⏰ *Режим работы офиса:*\n"
            "• Пн–Пт: 9:00 – 18:00\n"
            "• Сб, Вс: выходные дни\n\n"
            "_В экстренных случаях возможен выезд мастера в нерабочее время по отдельной договоренности._"
        )
        bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.back(), parse_mode='Markdown')
    else:
        text = (
            "🔧 *Оформление заявки на ремонт*\n\n"
            "Опишите, пожалуйста, *неисправность* вашего домофона.\n"
            "Чем подробнее вы расскажете о проблеме, тем быстрее и точнее наш мастер сможет вам помочь.\n\n"
            "_Например: «Не срабатывает открытие двери с трубки», «Нет изображения», «Не работает панель вызова»._"
        )
        msg = bot.send_message(chat_id=chat_id,
                               text=text, reply_markup=buttons.back(), parse_mode='Markdown')
        bot.register_next_step_handler(msg, install, chat_id, user)


def get_type(data, action):
    if data[0] == 'doorphone':
        type = f'{action} обычного домофона'
    else:
        type = f'{action} умного домофона'
    return type

def delivery_keys(message, chat_id, user):
    if message.content_type == 'text':
        number = message.text
        Order.objects.create(user=user, type='Доставка ключей', text=f'{number} штук')
        text = (
            "✅ *Заявка успешно создана!*\n\n"
            "Благодарим за обращение в компанию «Велес». Ваша заявка принята в работу и передана свободному специалисту.\n\n"
            "📞 *С вами свяжутся* в ближайшее время для уточнения деталей и согласования времени.\n\n"
            "⏰ *Режим работы офиса:*\n"
            "• Пн–Пт: 9:00 – 18:00\n"
            "• Сб, Вс: выходные дни\n\n"
            "_В экстренных случаях возможен выезд мастера в нерабочее время по отдельной договоренности._"
        )
        bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.back(), parse_mode='Markdown')
    else:
        msg = bot.send_message(chat_id=chat_id,
                               text='Введите количество ключей.')
        bot.register_next_step_handler(msg, install, chat_id, user)

def color_door(message, chat_id, user):
    if message.content_type == 'text':
        reason = message.text
        Order.objects.create(user=user, type='Покраска дверей', text=reason)
        text = (
            "✅ *Заявка успешно создана!*\n\n"
            "Благодарим за обращение в компанию «Велес». Ваша заявка принята в работу и передана свободному специалисту.\n\n"
            "📞 *С вами свяжутся* в ближайшее время для уточнения деталей и согласования времени.\n\n"
            "⏰ *Режим работы офиса:*\n"
            "• Пн–Пт: 9:00 – 18:00\n"
            "• Сб, Вс: выходные дни\n\n"
            "_В экстренных случаях возможен выезд мастера в нерабочее время по отдельной договоренности._"
        )
        bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.back(), parse_mode='Markdown')
    else:
        msg = bot.send_message(chat_id=chat_id,
                               text='Выберите причину обращения из списка под клавиатурой или напишите текст', parse_mode='Markdown')
        bot.register_next_step_handler(msg, install, chat_id, user)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    user = User.objects.filter(chat_id=chat_id).first()
    if check_subscribe(chat_id=chat_id):
        if call.message:
            try:
                bot.delete_message(chat_id=chat_id, message_id=call.message.id)
            except Exception:
                pass
            data = call.data.split('|')
            if data[0] == 'menu':
                menu(chat_id=chat_id)
            elif data[0] in ['doorphone', 'smart_doorphone']:
                if len(data) == 1:
                    doorphone(chat_id, user, data[0])
                else:
                    if data[1] == 'install':
                        type = get_type(data, 'Установка')
                        text = (
                            "📝 *Оформление заявки на установку*\n\n"
                            "Для начала работ нам потребуется ваше согласие.\n"
                            "Пожалуйста, *отправьте ссылку* на подписанный протокол или ваше согласие на индивидуальную установку.\n\n"
                            "_Это обязательный шаг для соблюдения формальностей._"
                        )
                        msg = bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.back(),
                                               parse_mode='Markdown')
                        bot.register_next_step_handler(msg, install, chat_id, user, type)
                    else:
                        type = get_type(data, 'Ремонт')
                        text = (
                            "🔧 *Оформление заявки на ремонт*\n\n"
                            "Опишите, пожалуйста, *неисправность* вашего домофона.\n"
                            "Чем подробнее вы расскажете о проблеме, тем быстрее и точнее наш мастер сможет вам помочь.\n\n"
                            "_Например: «Не срабатывает открытие двери с трубки», «Нет изображения», «Не работает панель вызова»._"
                        )
                        msg = bot.send_message(chat_id=chat_id,
                                               text=text, parse_mode='Markdown')
                        bot.register_next_step_handler(msg, repair, chat_id, user, type)
            elif data[0] == 'cameras':
                text = (
                    "📹 *Системы видеонаблюдения*\n\n"
                    "Скоро у нас появится эта услуга! Мы активно работаем над тем, чтобы предложить вам не только надежные домофоны, но и современные системы видеоконтроля.\n\n"
                    "Следите за обновлениями в нашем канале, чтобы быть первыми!"
                )
                bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.back(), parse_mode='Markdown')
            elif data[0] == 'delivery_keys':
                text = (
                    "🔑 *Заказ электронных ключей*\n\n"
                    "Нужны новые или дополнительные ключи для домофона?\n"
                    "Просто укажите необходимое *количество*.\n\n"
                    "Наш курьер доставит их в удобное для вас время."
                )
                msg = bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')
                bot.register_next_step_handler(msg, delivery_keys, chat_id, user)
            elif data[0] == 'color_door':
                text = (
                    "🎨 *Покраска металлической двери в подъезде*\n\n"
                    "Вернем эстетичный вид вашей двери! Выберите стандартную причину из списка ниже *или напишите свой вариант* (например, указать цвет).\n\n"
                    "_Наши мастера подберут стойкую краску и аккуратно выполнят работу._"
                )
                msg = bot.send_message(chat_id=chat_id,
                                       text=text, reply_markup=buttons.color_door(), parse_mode='Markdown')
                bot.register_next_step_handler(msg, color_door, chat_id, user)
            elif data[0] == 'support':
                text = (
                    "📞 *Служба поддержки «Велес»*\n\n"
                    "У вас есть вопросы, нестандартная ситуация или пожелания?\n\n"
                    "Наша команда поддержки всегда на связи, чтобы помочь вам:\n"
                    "• 📱 Телефон: +78469925083\n\n"
                    "_Работаем для вашего спокойствия и безопасности._"
                )
                bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.back(), parse_mode='Markdown')
            elif data[0] == 'rating':
                text = (
                    "⭐ *Поделитесь вашим мнением!*\n\n"
                    "Для нас очень важна ваша оценка нашей работы. Это помогает нам становиться лучше.\n"
                    "Напишите, пожалуйста, несколько слов о том, как прошел визит мастера, или о качестве наших услуг.\n\n"
                    "_Если хотите, можете пропустить этот шаг._"
                )
                rating = int(data[1])
                order = Order.objects.get(id=data[2])
                msg = bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.skip(), parse_mode='Markdown')
                bot.register_next_step_handler(msg, review_step_2, user, order, chat_id, rating)


bot.polling(none_stop=True)

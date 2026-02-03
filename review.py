import buttons
from const import bot


def review_step_2(message, user, order, chat_id, rating):
    if message.content_type == 'text':
        review = message.text
        order.rating = rating
        if review != 'Пропустить':
            order.review = review
        order.save(update_fields=['review', 'rating'])
        # Можно добавить сообщение об успешном сохранении отзыва
        bot.send_message(chat_id=chat_id, text='Спасибо за ваш отзыв!')
    else:
        msg = bot.send_message(chat_id=chat_id, text='Пожалуйста, напишите отзыв текстом', reply_markup=buttons.skip())
        bot.register_next_step_handler(msg, review_step_2, user, order, chat_id, rating)


def review_step_1(message, user, order, chat_id):
    try:
        rating = int(message.text)
        if rating not in [1, 2, 3, 4, 5]:
            raise ValueError("Рейтинг должен быть от 1 до 5")
        msg = bot.send_message(chat_id=chat_id, text='Напишите отзыв', reply_markup=buttons.skip())
        bot.register_next_step_handler(msg, review_step_2, user, order, chat_id, rating)
    except (ValueError, Exception):
        msg = bot.send_message(chat_id=chat_id,
                               text='Оцените встречу с мастером от 1 до 5', reply_markup=buttons.back())
        bot.register_next_step_handler(msg, review_step_1, user, order, chat_id)


def review(user, order):
    chat_id = user.chat_id
    bot.send_message(chat_id=chat_id, text='Оцените встречу с мастером от 1 до 5', reply_markup=buttons.rating(order.id))
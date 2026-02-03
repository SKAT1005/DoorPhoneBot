import buttons
from const import bot


def menu(chat_id):
    text = (
        "🏠 *Добро пожаловать в «Велес»!*\n\n"
        "Мы — ваш надежный партнер в мире безопасности и комфорта. "
        "Выберите нужную услугу, и мы оперативно решим вашу задачу по установке, ремонту или обслуживанию домофонных систем.\n\n"
        "Чем могу помочь?"
    )
    bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.menu(), parse_mode='Markdown')
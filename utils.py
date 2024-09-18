import telebot
from os import environ as env
from telebot import types

bot = telebot.TeleBot(env.get("TELEGRAM_BOT_TOKEN"))


def text_checker(func):
    def inner(*args):
        message = args[0]
        if message.content_type == "text":
            func(*args)
        else:
            incorrect_text = f"Тип сообщения должен быть <u><b>обычный текст</b></u>\n" \
                                         f"Повтори попытку и не повтори ошибку 😉"
            bot.send_message(message.chat.id, incorrect_text, parse_mode="HTML")
            bot.register_next_step_handler(message, func, *args[1:])

    return inner


def space_checker(func):
    def inner(*args):
        message = args[0]

        if " " in message.text.strip():
            incorrect_text = f"Сообщение <u><b>не должно содержать пробелов</b></u>\n" \
                             f"Попробуй снова)"
            bot.send_message(message.chat.id, incorrect_text, parse_mode="HTML")
            bot.register_next_step_handler(message, func, *args[1:])
        else:
            func(*args)

    return inner


def photo_checker(func):
    def inner(*args):
        message = args[0]
        if message.content_type == "photo":
            func(*args)
        else:
            incorrect_description_text = f"Тип сообщения должен быть <u><b>фото</b></u>\n" \
                                         f"<b>Обрати внимание:</b> если отправить фото файлом, то так тоже ничего не выйдет"
            bot.send_message(message.chat.id, incorrect_description_text, parse_mode="HTML")
            bot.register_next_step_handler(message, func, *args[1:])

    return inner


def length_checker(length=255):
    def outer(func):

        def inner(*args):
            message = args[0]
            if 0 < len(message.text.strip()) <= length:
                func(*args)
            else:
                incorrect_description_text = f"{message.chat.first_name}, подумай еще!\n" \
                                             f"Сообщение должно быть <u><b>не более чем из {length} букв!</b></u>\n"
                bot.send_message(message.chat.id, incorrect_description_text, parse_mode="HTML")
                bot.register_next_step_handler(message, func, *args[1:])

        return inner

    return outer


def registration_check(func):
    def inner(*args, **kwargs):
        from models import User

        message = args[0]
        ## If nothing given we use id of current user
        ## otherwise we use given user_id
        _user_id = message.chat.id if "user_id" not in kwargs.keys() else kwargs["user_id"]

        ## If user with this user_id exists we run function
        if User.get_or_none(User.user_id == _user_id):
            func(*args)

        ## Otherwise we give message that user with this user_id doesn't exist
        else:
            if message.chat.id == _user_id:
                keyboard = types.InlineKeyboardMarkup()

                reg_btn = types.InlineKeyboardButton("Зарегистрироваться", callback_data="registration")
                keyboard.add(reg_btn)

                text = f"{message.chat.first_name}, вы еще не создали аккаунт\n" \
                       f"Чтобы это исправить, <b>нажимайте кнопку ниже</b>"
                bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode="HTML")
            else:
                text = f"Такого пользователя не существует\n" \
                       f"Возможно, он удалил профиль или никогда его и не создавал"
                bot.send_message(message.chat.id, text, parse_mode="HTML")

    return inner


def show_list_buttons(array, c_data):

    keyboard = types.InlineKeyboardMarkup()

    btns = []

    for c_data_ending, value in array:
        btns.append(types.InlineKeyboardButton(f"{value}", callback_data=f"{c_data}|{c_data_ending}"))

    for i in range(0, len(btns), 2):
        if i + 1 == len(btns):
            keyboard.add(btns[i])
        else:
            keyboard.row(btns[i], btns[i + 1])

    return keyboard
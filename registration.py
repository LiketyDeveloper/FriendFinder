from utils import *

from pathlib import Path
from models import User, Topic
import database as db


def register_user(message): _get_username(message)


@space_checker
@text_checker
@length_checker(24)
def _get_username(message):
    username = message.text.strip()

    username_text = f"Супер! Теперь я тебя буду называть - <b><em>{username}</em></b> \n" \
                    f"А теперь придумай себе классное <b>описание профиля</b>, оно должно содержать основную информацию о тебе" \
                    f"и <u>не превышать 255 символов</u>"

    bot.send_message(message.chat.id, username_text, parse_mode="HTML")
    bot.register_next_step_handler(message, _get_description, username)


@text_checker
@length_checker(255)
def _get_description(message, username: str):
    description = message.text.strip()

    description_text = "Отлично! Ты уже на финишной прямой!\n" \
                       "Тебе осталось лишь <b>прислать фото</b> для профиля и ты уже на тропе к новым приключениям!\n"
    bot.send_message(message.chat.id, description_text, parse_mode="HTML")
    bot.register_next_step_handler(message, _get_photo, username, description)


@photo_checker
def _get_photo(message, username: str, description: str):
    ## Making directory if not exists
    Path(f'files/{message.chat.id}/photos').mkdir(parents=True, exist_ok=True)

    ## Getting photo from user
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    ## Saving photo
    src = f'files/{message.chat.id}/' + file_info.file_path
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    ## Registering new user
    User.create(
        user_id=message.chat.id,
        username=username,
        description=description,
        profile_photo_path=file_info.file_path
    )
    ## Send message that says registration succeed
    with open('static/anxous_girl.jpg', 'rb') as photo:

        keyboard = types.InlineKeyboardMarkup()

        show_profile_btn = types.InlineKeyboardButton("Посмотреть профиль", callback_data="profile|show_current")
        keyboard.add(show_profile_btn)

        registration_succeed_text = "<b>Поздравляем! Ты успешно зарегистрирован!</b> \n" \
                                    f"Теперь тебе доступны все возможности этого бота!"
        bot.send_photo(message.chat.id, photo, caption=registration_succeed_text, parse_mode="HTML", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data == "registration")
def registration_callback(callback):
    text = f"<b>Ну что ж, {callback.message.chat.first_name}, давай знакомиться!</b>\n\n" \
           f"Для начала <b>введи ник</b>, который будет отображаться у других пользователей, он должен содержать <u>не более 24 символов и ни одного пробела</u>"

    bot.send_message(callback.message.chat.id, text, parse_mode="HTML")

    bot.register_next_step_handler(callback.message, register_user)


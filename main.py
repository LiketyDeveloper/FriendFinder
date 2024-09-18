import random

import database as db
import profile # type: ignore
from models import User, Relationship, Topic, TopicToUser, TYPES_OF_RELATIONSHIP
from utils import *

import registration


@bot.message_handler(commands=['start'])
def start(message):
    query = User.select().where(User.user_id == message.chat.id)
    if not db.fetchall(query):
        keyboard = types.InlineKeyboardMarkup()

        reg_btn = types.InlineKeyboardButton("Зарегистрироваться", callback_data="registration")
        keyboard.add(reg_btn)

        with open('static/girl_greeting.jpeg', 'rb') as photo:
            text = f"Хэйоу, привет! {message.chat.first_name}, я вижу ты еще не зарегистрирован...\n" \
                   f"Меня зовут <b>Розмари</b> и я здесь для того чтобы найти тебе новых друзей!\n" \
                   f"Со мной тебя ждут новые знакомства и куча незабываемых впечатлений!\n" \
                   f"<b>Чтобы не упустить этот шанс тапай по кнопке снизу</b>↘️"

            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=keyboard, parse_mode="HTML")
    else:
        show_menu(message)


@bot.message_handler(commands=['menu'])
@registration_check
def show_menu(message):
    """
    Функция для показа основновного функционала бота
    """

    keyboard = types.InlineKeyboardMarkup()

    find_friends_btn = types.InlineKeyboardButton("Найти друга", callback_data="menu|find_friend")
    show_friends_btn = types.InlineKeyboardButton("Друзья", callback_data="menu|show_friends")
    show_requests_btn = types.InlineKeyboardButton("Заявки", callback_data="menu|show_recieved")
    chat_btn = types.InlineKeyboardButton("Чат", callback_data="menu|chat")

    keyboard.add(find_friends_btn)
    keyboard.row(show_friends_btn, show_requests_btn, chat_btn)

    text = (f"<b>📋 Ты находишься в главном меню 📋</b>\n\n"
            f"Выбери что хочешь делать")

    bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode="HTML")


@bot.message_handler(commands=['message'])
def message_to_friend(message):

    try:
        username = message.text.strip().split(" ")[1]

        content = " ".join(message.text.strip().split(" ")[2:])

        other_user = User.get(User.username == username)
        current_user = User.get_by_id(message.chat.id)

        is_friend = db.fetchall(Relationship.select().where(
                (Relationship.user_id == message.chat.id) &
                (Relationship.other_id == other_user.user_id) &
                (Relationship.relationship == TYPES_OF_RELATIONSHIP["Friend"])
            ))

        if is_friend:
            current_user_text = f"✅ <i><u>Отправленное сообщение пользователю #<b>{other_user.username}</b></u></i>\n\n" \
                                f" >> {content}"
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, current_user_text, parse_mode="HTML")
            other_user_text = f"↙️ <i><u>Полученное сообщение от пользователя #<b>{current_user.username}</b></u></i>\n\n" \
                              f" >> {content}"
            bot.send_message(other_user.user_id, other_user_text, parse_mode="HTML")
        else:
            text = "Вы можете писать только друзьям, а этот пользователь не находится в списке ваших друзей"
            bot.send_message(message.chat.id, text)
    except IndexError as err:
        text = "Отправление сообщения производится по форме: \n" \
               "<code>/message имя_пользователя текст_сообщения</code>"
        bot.send_message(message.chat.id, text, parse_mode="HTML")
    except User.DoesNotExist:
        bot.send_message(message.chat.id, "Такого пользователя не существует")


def message_to_friend_from_profile(message, user_id):
    try:
        other_user = User.get_by_id(user_id)
        current_user = User.get_by_id(message.chat.id)

        content = message.text.strip()

        current_user_text = f"✅ <i><u>Отправленное сообщение пользователю #<b>{other_user.username}</b></u></i>\n\n" \
                            f" >> {content}"
        try:
            bot.delete_message(message.chat.id, message.message_id-1)
        except telebot.apihelper.ApiTelegramException:
            pass
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, current_user_text, parse_mode="HTML")
        other_user_text = f"↙️ <i><u>Полученное сообщение от пользователя #<b>{current_user.username}</b></u></i>\n\n" \
                          f" >> {content}"
        bot.send_message(other_user.user_id, other_user_text, parse_mode="HTML")

    except User.DoesNotExist:
        bot.send_message(message.chat.id, "[Ошибка] Такого пользователя не существует")


deffered_users = {}


def find_friend(message):

    tmp = deffered_users.copy()

    for user_id in tmp.keys():
        deffered_users[user_id] += 1

    for user_id, i in tmp.items():
        if i > 3:
            deffered_users.pop(user_id)

    topics_ids = list(map(lambda arr: arr[2], db.fetchall(TopicToUser.select().where(TopicToUser.user_id == message.chat.id))))

    known_users_id = list(map(lambda arr: arr[2],
                           db.fetchall(Relationship.select().where(
                               Relationship.user_id == message.chat.id)
                           )))

    users = []
    for topic_id in topics_ids:
        user_ids = list(map(lambda arr: arr[1],
                            db.fetchall(TopicToUser.select().where(TopicToUser.topic_id == topic_id)))
                        )
        for user_id in user_ids:
            users.append(User.get_by_id(user_id))

    suggested_users = [user for user in users if user.user_id not in known_users_id and user.user_id not in list(deffered_users.keys()) and user.user_id != message.chat.id]

    if not suggested_users:
        user_ids = list(map(lambda arr: arr[0],
                            db.fetchall(User.select()))
                        )

        for user_id in user_ids:
            users.append(User.get_by_id(user_id))

        users = set(users)
        suggested_users = [user for user in users if user.user_id not in known_users_id and user.user_id != message.chat.id]

    if not suggested_users:

        text = f"Увы, вы долистали до конца\nКогда новые пользователи присоединятся, то мы сразу вас с ними познакомим)"
        bot.send_message(message.chat.id, text)


    ## Иначе рандомно выбирается профиль, которого предлагают пользователю
    else:
        chosen_user = random.choice(suggested_users)

        keyboard = types.InlineKeyboardMarkup()

        request_btn = types.InlineKeyboardButton("✅", callback_data=f"find_friend|send_request|{chosen_user.user_id}")
        dont_know = types.InlineKeyboardButton("Не знаю", callback_data=f"find_friend|dont_know|{chosen_user.user_id}")
        reject_btn = types.InlineKeyboardButton("❌", callback_data=f"find_friend|not_intrested|{chosen_user.user_id}")
        stop_btn = types.InlineKeyboardButton("Остановить ленту", callback_data=f"reply|back_to_menu")

        keyboard.row(request_btn, dont_know, reject_btn)
        keyboard.add(stop_btn)

        profile.show(message, chosen_user.user_id, keyboard)


def show_anket(message, user_id):
    user = User.get_by_id(user_id)

    keyboard = types.InlineKeyboardMarkup()

    request_btn = types.InlineKeyboardButton("✅", callback_data=f"find_friend|send_request|{user.user_id}")
    reject_btn = types.InlineKeyboardButton("❌", callback_data=f"find_friend|not_intrested|{user.user_id}")

    keyboard.row(request_btn, reject_btn)

    profile.show(message, user.user_id, keyboard)


reply_keyboard = types.InlineKeyboardMarkup()

back_to_menu_btn = types.InlineKeyboardButton("В меню", callback_data="reply|back_to_menu")
continue_btn = types.InlineKeyboardButton("Продолжить >>", callback_data="reply|continue")
reply_keyboard.row(back_to_menu_btn, continue_btn)


def send_request(message, other_user_id):
    has_sent = bool(db.fetchall(Relationship.select().where(
        (Relationship.user_id == message.chat.id) & (Relationship.other_id == other_user_id))))

    other_user = User.get_by_id(other_user_id)
    current_user = User.get_by_id(message.chat.id)

    if has_sent:

        text = f"Вы не можете несколько раз отправлять заявку одному и тому же пользователю"
        bot.send_message(message.chat.id, text, parse_mode="HTML")

    else:

        has_recieved = bool(db.fetchall(Relationship.select().where(
            (Relationship.user_id == other_user_id) &
            (Relationship.other_id == message.chat.id) &
            (Relationship.relationship == TYPES_OF_RELATIONSHIP["Pending"])
        )))

        if has_recieved:

            Relationship.update(relationship=TYPES_OF_RELATIONSHIP["Friend"]).where(
                Relationship.user_id == other_user_id).execute()
            Relationship.create(user_id=message.chat.id,
                                other_id=other_user_id,
                                relationship=TYPES_OF_RELATIONSHIP["Friend"])

            text = f"Вы и <b>{other_user.username}</b> теперь друзья!\nТак как этот пользователь уже отправлял вам ранее заявку в друзья"
            bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=reply_keyboard)
            text = f"Вы и <b>{current_user.username}</b> теперь друзья!\nТак как этот пользователь уже отправлял вам ранее заявку в друзья"
            bot.send_message(other_user.user_id, text, parse_mode="HTML", reply_markup=reply_keyboard)

        else:

            Relationship.create(user_id=message.chat.id,
                                other_id=other_user_id,
                                relationship=TYPES_OF_RELATIONSHIP["Pending"])

            text = "Прекрасно!\nЯ уведомлю пользователя, что вам он интересен и если он примет заявку вы станете друзьями!))"
            bot.send_message(message.chat.id, text, reply_markup=reply_keyboard)

            keyboard = types.InlineKeyboardMarkup()

            show_btn = types.InlineKeyboardButton("Посмотреть ↘️↘️↘️",
                                                  callback_data=f"reply|show_anket|{message.chat.id}")
            keyboard.add(show_btn)

            bot.send_message(other_user_id,
                             f"Привет, тебе предложил дружить пользователь под ником <b>{current_user.username}</b>",
                             parse_mode="HTML", reply_markup=keyboard)


def dont_know(message, other_user_id):
    text = "Хорошо)\nЯ потом ещё подкину вам этот профиль)"

    deffered_users[int(other_user_id)] = 0

    bot.send_message(message.chat.id, text, reply_markup=reply_keyboard)


def not_interested(message, other_user_id):
    has_sent = bool(db.fetchall(Relationship.select().where(
        (Relationship.user_id == message.chat.id) & (Relationship.other_id == other_user_id))))

    other_user = User.get_by_id(other_user_id)
    current_user = User.get_by_id(message.chat.id)

    if has_sent:

        text = f"Вы не можете несколько раз отклонять одного и того же пользователю"
        bot.send_message(message.chat.id, text, parse_mode="HTML")

    else:

        has_recieved = bool(db.fetchall(Relationship.select().where(
            (Relationship.user_id == other_user_id) &
            (Relationship.other_id == message.chat.id) &
            (Relationship.relationship == TYPES_OF_RELATIONSHIP["Pending"])
        )))
        if has_recieved:

            text = f"Пользователь <b>{current_user.username}</b> отклонил вашу заявку в друзья, он больше не будет попадаться в вашей ленте"
            bot.send_message(message.chat.id, text, parse_mode="HTML")

            Relationship.update(relationship=TYPES_OF_RELATIONSHIP["Denied"]).where(
                Relationship.user_id == other_user_id).execute()

        else:

            Relationship.create(user_id=other_user_id,
                                other_id=message.chat.id,
                                relationship=TYPES_OF_RELATIONSHIP["Denied"])

        Relationship.create(user_id=message.chat.id,
                            other_id=other_user_id,
                            relationship=TYPES_OF_RELATIONSHIP["Denied"])

        text = "Хорошо(\nЭтот пользователь больше не будет появляться в вашей ленте"

        bot.send_message(message.chat.id, text, reply_markup=reply_keyboard)


@registration_check
def show_friends(message):
    query = db.fetchall(Relationship.select().where(Relationship.user_id == message.chat.id).where(Relationship.relationship == TYPES_OF_RELATIONSHIP["Friend"]))
    friends = {User.get_by_id(id).username: User.get_by_id(id).description for id in list(map(lambda arr: arr[2], query))}

    text = "<b>Вот твои друзья:</b>\n"
    if friends.items():
        for i, (name, description) in enumerate(friends.items(), 1):
            text += f"<b>{i}</b>. 👤 <b>Имя:</b> <code>{name}</code>\n" \
                    f" --{'--' * (i // 10)} 📃 <b>Описание:</b> {description}\n\n"
        else:
            text += "Напиши имя друга, чей профиль хочешь посмотреть"

        bot.send_message(message.chat.id, text, parse_mode="HTML")
        bot.register_next_step_handler(message, show_friends_respond_handler)
    else:
        text = "У тебя пока что нет друзей, ты можешь завести их в ленте рекомендаций, куда можно зайти из /menu"
        bot.send_message(message.chat.id, text, parse_mode="HTML")


def show_friends_respond_handler(message):
    try:
        requested_user = User.get(User.username == message.text.strip())

        is_friend = db.fetchall(Relationship.select().where(
            (Relationship.user_id == message.chat.id) &
            (Relationship.other_id == requested_user.user_id) &
            (Relationship.relationship == TYPES_OF_RELATIONSHIP["Friend"])
        ))

        keyboard = types.InlineKeyboardMarkup()
        friend_chat_btn = types.InlineKeyboardButton("Написать", callback_data=f"find_friend|friend_chat|{requested_user.user_id}")
        delete_friend_btn = types.InlineKeyboardButton("Удалить друга", callback_data=f"find_friend|delete_friend|{requested_user.user_id}")
        keyboard.add(friend_chat_btn, delete_friend_btn)

        if is_friend:
            profile.show(message, requested_user.user_id, keyboard)
        else:
            text = "Такого пользователя у тебя в друзьях нет"
            bot.send_message(message.chat.id, text)

    except User.DoesNotExist:
        text = "Такого пользователя не существует"
        bot.send_message(message.chat.id, text)


def show_recieved_requests(message):
    query = db.fetchall(Relationship.select().where((Relationship.other_id == message.chat.id) &
                        (Relationship.relationship == TYPES_OF_RELATIONSHIP["Pending"])))
    recieved = {User.get_by_id(id).username: User.get_by_id(id).description for id in list(map(lambda arr: arr[1], query))}

    if recieved:
        text = "<b>Вот пользователи, которые отправляли тебе сегодня заявки:</b>\n"

        for i, (name, description) in enumerate(recieved.items(), 1):
            text += f"<b>{i}</b>. 👤 <b>Имя:</b> <code>{name}</code>\n" \
                    f" --{'--' * (i // 10)} 📃 <b>Описание:</b> {description}\n\n"
        else:
            text += "Напиши никнейм пользователя, чей профиль хочешь посмотреть"

        bot.send_message(message.chat.id, text, parse_mode="HTML")
        bot.register_next_step_handler(message, show_recieved_requests_respond_handler)
    else:
        text = f"Тебе пока что никто не отправил заявку в друзья"
        bot.send_message(message.chat.id, text, parse_mode="HTML")


def show_recieved_requests_respond_handler(message):
    try:

        requested_user = User.get(User.username == message.text.strip())

        has_sent = db.fetchall(Relationship.select().where((Relationship.user_id == requested_user.user_id) &
                               (Relationship.other_id == message.chat.id) &
                               (Relationship.relationship == TYPES_OF_RELATIONSHIP["Pending"])))

        if has_sent:
            show_anket(message, requested_user.user_id)
        else:
            text = "Этот пользователь не отправлял вам заявку в друзья"
            bot.send_message(message.chat.id, text)

    except User.DoesNotExist:
        text = "Такого пользователя не существует"
        bot.send_message(message.chat.id, text)



def delete_friend(message, user_id):
    keyboard = types.InlineKeyboardMarkup()

    yes_btn = types.InlineKeyboardButton("Да, уверен(-а)", callback_data=f"find_friend|confirm_deleting|{user_id}")
    no_btn = types.InlineKeyboardButton("Нет, не буду", callback_data=f"find_friend|discard_deleting|{user_id}")

    keyboard.row(yes_btn, no_btn)
    text = f"{User.get_by_id(message.chat.id).username}, вы уверены что хотите удалить {User.get_by_id(user_id).username} из друзей?"

    bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode="HTML")


@bot.callback_query_handler(func=lambda callback: callback.data.startswith("menu"))
def menu_callback(callback):
    command = callback.data.split("|")[1]

    bot.delete_message(callback.message.chat.id, callback.message.message_id)

    if command == "find_friend":
        find_friend(callback.message)
    elif command == "show_friends":
        show_friends(callback.message)
    elif command == "show_recieved":
        show_recieved_requests(callback.message)
    elif command == "chat":
        text = "Отправление сообщения производится по форме: \n" \
               "<code>/message имя_пользователя текст_сообщения</code>"
        bot.send_message(callback.message.chat.id, text, parse_mode="HTML")


@bot.callback_query_handler(func=lambda callback: callback.data.startswith("find_friend"))
def find_friend_callback(callback):
    command = callback.data.split("|")[1]
    user_id = callback.data.split("|")[2]

    if command == "send_request":
        send_request(callback.message, user_id)
    elif command == "dont_know":
        dont_know(callback.message, user_id)
    elif command == "not_intrested":
        not_interested(callback.message, user_id)
    elif command == "friend_chat":
        text = f"Напишите ваше сообщение пользователю <b>{User.get_by_id(user_id).username}</b>"
        bot.send_message(callback.message.chat.id, text, parse_mode="HTML")

        bot.register_next_step_handler(callback.message, message_to_friend_from_profile, user_id)
    elif command == "delete_friend":
        delete_friend(callback.message, user_id)
    elif command == "confirm_deleting":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        Relationship.delete().where((Relationship.user_id == callback.message.chat.id) &
                                    (Relationship.other_id == user_id)).execute()
        Relationship.delete().where((Relationship.user_id == user_id) &
                                    (Relationship.other_id == callback.message.chat.id)).execute()
        bot.send_message(callback.message.chat.id,
                         f"Вы удалили пользователя {User.get_by_id(user_id).username} из своих друзей",
                         parse_mode="HTML")
        bot.send_message(user_id,
                         f"Пользователь {User.get_by_id(callback.message.chat.id).username} удалил(-а) вас из своих друзей",
                         parse_mode="HTML")
    elif command == "discard_deleting":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id,
                         "Я уверен ты сделал(-а) правильный выбор)\n"
                         "Иначе сейчас у тебя было бы на одного друга меньше",
                         parse_mode="HTML")


@bot.callback_query_handler(func=lambda callback: callback.data.startswith("reply"))
def reply_callback(callback):
    command = callback.data.split("|")[1]

    if command == "back_to_menu":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        show_menu(callback.message)
    elif command == "continue":
        find_friend(callback.message)
    elif command == "show_anket":
        user_id = callback.data.split("|")[2]
        show_anket(callback.message, user_id)


bot.polling(none_stop=True)

from utils import *
from models import User, Topic, TopicToUser, Relationship
import database as db


@registration_check
def show(message, user_id=None, keyboard=types.ReplyKeyboardRemove()):
    """
    This function shows the user profile by the specified user_id
    :param keyboard: Keyboard to show under the photo
    :param user_id: ID of the user profile that needs to be shown
    """

    user = User.get(User.user_id == user_id)
    query = TopicToUser.select().where(TopicToUser.user_id == user.user_id)

    text = f"👤 <b>Имя:</b> {user.username} \n\n" \
           f"📃 <b>Описание:</b> {user.description}"

    topics = get_topics(user.user_id)

    if topics:
        text += "\n🎨 <b>Интересуется:</b> "

        for topic in topics.values():
            text += f"{topic}, "

        text = text[:-2]

    with open(f"files/{user.user_id}/{user.profile_photo_path}", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=keyboard, parse_mode="HTML")


@bot.message_handler(commands=['show_profile'])
def show_current(message):
    keyboard = types.InlineKeyboardMarkup()

    edit_profile_btn = types.InlineKeyboardButton("Редактировать", callback_data="profile|edit")
    delete_profile_btn = types.InlineKeyboardButton("Удалить", callback_data="profile|delete")
    delete_topic_btn = types.InlineKeyboardButton("Настроить интересы и увлечения", callback_data="topic|settings|0")

    keyboard.row(edit_profile_btn, delete_profile_btn)
    keyboard.add(delete_topic_btn)

    show(message, message.chat.id, keyboard)


@registration_check
def topic_settings(message):

    keyboard = types.InlineKeyboardMarkup()

    add_topics_btn = types.InlineKeyboardButton("Добавить", callback_data="topic|add_topic")
    delete_topic_btn = types.InlineKeyboardButton("Удалить", callback_data="topic|delete_topic")

    keyboard.row(add_topics_btn, delete_topic_btn)

    bot.send_message(message.chat.id, "Привет! Здесь ты можешт настроить свои увлечения и хобби", reply_markup=keyboard)


added_topics = []


def add_topic(message):

    global added_topics

    query = db.fetchall(Topic.select().where(
        Topic.id.not_in(
            list(get_topics(message.chat.id).keys())
        )
    ))

    topics = {i: name for i, name in query}

    if not topics:

        if len(added_topics):
            text = f"Вы добавили {'тему' if len(added_topics) == 1 else 'темы'} "

            for topic in added_topics:
                text += f"{topic}, "
            else:
                text = text[:-2] + " в свои тематики"
                added_topics.clear()

            bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "Вы уже добавили все возможные тематики")

    else:
        keyboard = show_list_buttons(topics.items(), "topic|add")
        close_btn = types.InlineKeyboardButton("Закрыть", callback_data="topic|close_adding")
        keyboard.add(close_btn)

        bot.send_message(message.chat.id, "Это темы, благодаря которым ты можешь найти единомышленников\n"
                                          "Выбери те которые тебе нравятся больше всего", reply_markup=keyboard)


deleted_topics = []


def delete_topic(message):

    global deleted_topics

    topics = get_topics(message.chat.id)

    if not topics:

        if len(deleted_topics):
            text = f"Вы удалили {'тему' if len(deleted_topics) == 1 else 'темы'} "

            for topic in deleted_topics:
                text += f"{topic}, "
            else:
                text = text[:-2] + " из своих тематик"
                added_topics.clear()

            bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "У вас нет никаких тематик")

    else:
        keyboard = show_list_buttons(topics.items(), "topic|delete")
        close_btn = types.InlineKeyboardButton("Закрыть", callback_data="topic|close_deleting")
        keyboard.add(close_btn)

        bot.send_message(message.chat.id, "Выберите какие темы удалить из вашего профиля", reply_markup=keyboard)


def get_topics(user_id):

    query = TopicToUser.select().where(TopicToUser.user_id == user_id)
    topic_ids = list(map(lambda arr: arr[2], db.fetchall(query)))

    topics = {i: Topic.get_by_id(i).name for i in topic_ids}

    return topics


def edit(message):
    keyboard = types.InlineKeyboardMarkup()

    edit_username_btn = types.InlineKeyboardButton("Изменить ник", callback_data="profile|edit_username")
    edit_description_btn = types.InlineKeyboardButton("Изменить описаниие", callback_data="profile|edit_description")
    edit_photo_btn = types.InlineKeyboardButton("Изменить фото", callback_data="profile|edit_photo")
    cancel_btn = types.InlineKeyboardButton("Отменить", callback_data="profile|cancel_editing")

    keyboard.row(edit_username_btn, edit_description_btn)
    keyboard.add(edit_photo_btn)
    keyboard.add(cancel_btn)

    text = "Опачки, изменения подъехали)\nЧто именно ты хочешь редактировать? ✍️"

    bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode="HTML")


@space_checker
@length_checker(24)
@text_checker
def change_name(message):
    new_value = message.text.strip()

    user = User(username=new_value)
    commit_change(message, user)



@length_checker(255)
@text_checker
def change_description(message):
    new_value = message.text.strip()

    user = User(description=new_value)
    commit_change(message, user)


@photo_checker
def change_photo(message):
    # Получение фото от пользователя
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Сохранение фото
    src = f'files/{message.chat.id}/' + file_info.file_path
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    new_value = file_info.file_path

    user = User(profile_photo_path=new_value)
    commit_change(message, user)


def commit_change(message, user):
    user.user_id = message.chat.id
    user.save()

    keyboard = types.InlineKeyboardMarkup()

    show_profile_btn = types.InlineKeyboardButton("Показать ↘️↘️↘️", callback_data="profile|show_current")

    keyboard.add(show_profile_btn)

    bot.send_message(message.chat.id,
                     "Все! Готово, твой профиль успешно изменен ✅", reply_markup=keyboard, parse_mode="HTML")


def delete(message):
    keyboard = types.InlineKeyboardMarkup()

    yes_btn = types.InlineKeyboardButton("Да, уверен(-а)", callback_data="profile|confirm_deleting")
    no_btn = types.InlineKeyboardButton("Нет, останусь с вами", callback_data="profile|discard_deleting")

    keyboard.row(yes_btn, no_btn)
    text = f"{User.get_by_id(message.chat.id).username}, вы уверены что хотите удалить профиль?\n\n Все данные профиля будут стерты и из невозможно будет восстановить ‼️❌"

    bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode="HTML")


@bot.callback_query_handler(func=lambda callback: callback.data.startswith("profile"))
def profile_callback(callback):

    command = callback.data.split("|")[1]

    ## Show profile
    if command == "show":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        show(callback.message, callback.message.chat.id)
    elif command == "show_current":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        show_current(callback.message)

    ## Delete profile
    elif command == "delete":
        delete(callback.message)
    elif command == "confirm_deleting":
        User.delete().where(User.user_id == callback.message.chat.id).execute()
        TopicToUser.delete().where(TopicToUser.user_id == callback.message.chat.id).execute()
        Relationship.delete().where(Relationship.user_id == callback.message.chat.id).execute()
        Relationship.delete().where(Relationship.other_id == callback.message.chat.id).execute()

        bot.send_message(callback.message.chat.id,
                         "Эх.. Обидно, что ты больше не с нами 😪\n"
                         "Если опять захочешь к нам - <b>просто напиши</b> /start\n"
                         "<b>FriendFinder</b> всегда и всем рад 😉",
                         parse_mode="HTML")
    elif command == "discard_deleting":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id,
                         "Фух, а ведь это было страшно, что ты уйдешь\n"
                         "Больше не пугай так 😉",
                         parse_mode="HTML")


    ## Edit profile
    if command == "edit":
        edit(callback.message)
    elif command == "edit_username":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id,
                         "Хорошо, теперь напиши свой новый ник", parse_mode="HTML")
        bot.register_next_step_handler(callback.message, change_name)
    elif command == "edit_description":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id,
                         "Хорошо, теперь напиши своё новое описание профиля", parse_mode="HTML")
        bot.register_next_step_handler(callback.message, change_description)
    elif command == "edit_photo":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id,
                         "Хорошо, теперь отправь мне своё новое фото", parse_mode="HTML")
        bot.register_next_step_handler(callback.message, change_photo)
    elif command == "cancel_editing":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id,
                         "Хорошо, редактирование профиля отменено", parse_mode="HTML")


@bot.callback_query_handler(func=lambda callback: callback.data.startswith("topic"))
def topic_choose_callback(callback):

    global added_topics
    global deleted_topics

    command = callback.data.split("|")[1]
    if command == "settings":
        topic_settings(callback.message)

    elif command == "delete_topic":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        delete_topic(callback.message)

    elif command == "add_topic":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        add_topic(callback.message)

    elif command in ("add", "delete"):

        bot.delete_message(callback.message.chat.id, callback.message.message_id)

        topic_id = int(callback.data.split("|")[2])
        topic = Topic.get_by_id(topic_id)

        has_topic = TopicToUser.select().where(
            (TopicToUser.user_id == callback.message.chat.id) & (TopicToUser.topic_id == topic_id)
        )

        if command == "add":

            if has_topic:

                bot.send_message(callback.message.chat.id, f"Тема {topic.name} уже у вас в интересных")

            else:

                TopicToUser.create(user_id=callback.message.chat.id, topic_id=topic_id)

                added_topics.append(topic.name)

            add_topic(callback.message)

        elif command == "delete":

            if has_topic:

                TopicToUser.delete().where(
                    (TopicToUser.user_id == callback.message.chat.id) & (TopicToUser.topic_id == topic_id)
                ).execute()

                deleted_topics.append(topic.name)

            else:

                bot.send_message(callback.message.chat.id, f"[Ошибка] Тема {topic.name} уже удалена из ваших интересов")

            delete_topic(callback.message)

    elif command == "close_adding":

        if len(added_topics):

            keyboard = types.InlineKeyboardMarkup()
            bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=keyboard)

            text = f"Вы добавили {'тему' if len(added_topics) == 1 else 'темы'} "

            for topic in added_topics:
                text += f"{topic}, "
            else:
                text = text[:-2] + " в свои тематики"
                added_topics.clear()

            bot.edit_message_text(text, callback.message.chat.id, callback.message.message_id)
        else:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)

    elif command == "close_deleting":

        if len(deleted_topics):

            keyboard = types.InlineKeyboardMarkup()
            bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=keyboard)

            text = f"Вы удалили {'тему' if len(deleted_topics) == 1 else 'темы'} "

            for topic in deleted_topics:
                text += f"{topic}, "
            else:
                text = text[:-2] + " из своих тематик"
                deleted_topics.clear()

            bot.edit_message_text(text, callback.message.chat.id, callback.message.message_id)
        else:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)

 # type: ignore
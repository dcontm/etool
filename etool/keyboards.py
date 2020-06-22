from vk_api.keyboard import VkKeyboard, VkKeyboardColor


""" Набор клавиатур для меню бота vk """


def general_menu():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(
        "Расход",
        color=VkKeyboardColor.NEGATIVE,
        payload={"next": "category_menu"},
    )
    keyboard.add_button(
        "История",
        color=VkKeyboardColor.PRIMARY,
        payload={"next": "history_menu"},
    )

    keyboard.add_line()
    keyboard.add_button(
        "Статистика",
        color=VkKeyboardColor.DEFAULT,
        payload={"next": "statistics_menu"},
    )
    keyboard.add_button(
        "Помощь",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "help", "inc": "help"},
    )

    return keyboard.get_keyboard()


def nav_menu(back="general_menu"):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(
        "Меню", color=VkKeyboardColor.PRIMARY, payload={"next": "general_menu"}
    )
    keyboard.add_button(
        "Назад",
        color=VkKeyboardColor.PRIMARY,
        payload={"next": "{}".format(back)},
    )

    return keyboard.get_keyboard()


def category_menu(back="general_menu"):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(
        "Питание",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "spending", "inc": "FOOD"},
    )
    keyboard.add_button(
        "Одежда",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "spending", "inc": "DRESS"},
    )
    keyboard.add_button(
        "Для дома",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "spending", "inc": "FOR_HOME"},
    )

    keyboard.add_line()
    keyboard.add_button(
        "Авто",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "spending", "inc": "AUTO"},
    )
    keyboard.add_button(
        "Транспорт",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "spending", "inc": "TRANSPORT"},
    )
    keyboard.add_button(
        "ЖКХ/Связь",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "spending", "inc": "H_SERVICE"},
    )

    keyboard.add_line()
    keyboard.add_button(
        "Досуг",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "spending", "inc": "ENTERTAIMENT"},
    )
    keyboard.add_button(
        "Подарки",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "spending", "inc": "PRESENT"},
    )
    keyboard.add_button(
        "Услуги",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "spending", "inc": "SERVICE"},
    )

    keyboard.add_line()
    keyboard.add_button(
        "Кредиты",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "spending", "inc": "CREDIT"},
    )
    keyboard.add_button(
        "Копилка",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "spending", "inc": "ACCUM"},
    )
    keyboard.add_button(
        "Другое",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "spending", "inc": "OTHER"},
    )

    keyboard.add_line()
    keyboard.add_button(
        "Меню", color=VkKeyboardColor.PRIMARY, payload={"next": "general_menu"}
    )
    keyboard.add_button(
        "Назад",
        color=VkKeyboardColor.PRIMARY,
        payload={"next": "{}".format(back)},
    )

    return keyboard.get_keyboard()


def history_menu(back="general_menu"):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(
        "Посл. 20",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "history", "inc": "h_last_20"},
    )
    keyboard.add_button(
        "Неделя",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "history", "inc": "h_week"},
    )
    keyboard.add_button(
        "Месяц",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "history", "inc": "h_month"},
    )

    keyboard.add_line()
    keyboard.add_button(
        "Меню", color=VkKeyboardColor.PRIMARY, payload={"next": "general_menu"}
    )
    keyboard.add_button(
        "Назад",
        color=VkKeyboardColor.PRIMARY,
        payload={"next": "{}".format(back)},
    )

    return keyboard.get_keyboard()


def statistics_menu(back="general_menu"):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(
        "Общая",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "statistics", "inc": "s_full"},
    )
    keyboard.add_button(
        "Неделя",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "statistics", "inc": "s_week"},
    )
    keyboard.add_button(
        "Месяц",
        color=VkKeyboardColor.DEFAULT,
        payload={"action": "statistics", "inc": "s_month"},
    )

    keyboard.add_line()
    keyboard.add_button(
        "Меню", color=VkKeyboardColor.PRIMARY, payload={"next": "general_menu"}
    )
    keyboard.add_button(
        "Назад",
        color=VkKeyboardColor.PRIMARY,
        payload={"next": "{}".format(back)},
    )

    return keyboard.get_keyboard()


def complete_menu():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(
        "Завершить",
        color=VkKeyboardColor.POSITIVE,
        payload={"action": "complete", "inc": "complete"},
    )
    keyboard.add_button(
        "Отменить",
        color=VkKeyboardColor.NEGATIVE,
        payload={"action": "roll_back", "inc": "roll_back"},
    )

    return keyboard.get_keyboard()

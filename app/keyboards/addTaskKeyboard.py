from aiogram import types


add_task_kb = types.ReplyKeyboardMarkup(
        keyboard=[
        [
            types.KeyboardButton(text="/add"),
            types.KeyboardButton(text="/tsk"),
        ],
        [
            types.KeyboardButton(text="Помощь")
        ]
    ],
        resize_keyboard=True,
    )


back_exit_kb = types.ReplyKeyboardMarkup(
        keyboard=[
        [
            types.KeyboardButton(text="Назад"),
            types.KeyboardButton(text="Отмена")
        ],
    ],
        resize_keyboard=True,
    )
exit_kb = types.ReplyKeyboardMarkup(
        keyboard=[
        [
            types.KeyboardButton(text="Отмена")
        ],
    ],
        resize_keyboard=True,
    )
confirm_back_exit_kb = types.ReplyKeyboardMarkup(
        keyboard=[
        [
            types.KeyboardButton(text="Отмена"),
            types.KeyboardButton(text="Назад"),
        ],
        [
            types.KeyboardButton(text="Подтвердить")
        ]
    ],
        resize_keyboard=True,
    )
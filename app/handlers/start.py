from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, Message
from states.addTask import addTaskState
from keyboards.addTaskKeyboard import back_exit_kb, exit_kb, confirm_back_exit_kb, add_task_kb
from DB.db import Database
from middlewares.database import DBMiddleware
from datetime import datetime

router = Router()




@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Добро пожаловать в бота который не даст вам забыть о своих задачах!\n\n"
        "Доступные команды:\n\n"
        "/add - Добавить новую задачу\n"
        "/tsk - Просмотреть все задачи\n"
        "Помощь - Получить информацию о командах\n",
        reply_markup=add_task_kb
    )


@router.message(F.text == "Помощь")
async def help(message: Message, ):
    await message.answer("Доступные команды:\n"
                         "/add - Добавить новую задачу\n"
                         "/tsk - Просмотреть все задачи", reply_markup=add_task_kb)


@router.message(Command("tsk"))
async def add(message: Message, db: Database):
    text = "Ваши задачи:\n"
    res = await db.get_tasks()

    for i, row in enumerate(res):
        text += f"\n{i+1}) Название: {row.get('title')}\n" \
                f"Описание: {row.get('description')}\n" \
                f"Выполнить до: {row.get('expire')}\n"

    await message.answer(text, reply_markup=add_task_kb)


@router.message(StateFilter(None), Command("add"))
async def add(message: Message, state: FSMContext):
    await message.answer("Введите название задачи:", reply_markup=exit_kb)
    await state.set_state(addTaskState.choosing_title.state)


@router.message(addTaskState.choosing_title, F.text)
async def add_choosing_title(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        await message.answer("Создание задачи отменено!", reply_markup=ReplyKeyboardRemove())
        return

    await state.update_data(title=message.text)
    await message.answer("Введите описание задачи:", reply_markup=back_exit_kb)
    await state.set_state(addTaskState.choosing_desc.state)


@router.message(addTaskState.choosing_desc, F.text)
async def add_choosing_desc(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await message.answer("Введите название задачи:", reply_markup=exit_kb)
        await state.set_state(addTaskState.choosing_title.state)
        return
    elif message.text == 'Отмена':
        await state.clear()
        await message.answer("Создание задачи отменено!", reply_markup=ReplyKeyboardRemove())
        return

    await state.update_data(description=message.text)
    await message.answer("Введите дату до которой нужно выполнить задачу в формате ДД:ММ:ГГГГ:",
                         reply_markup=back_exit_kb)
    await state.set_state(addTaskState.choosing_date.state)


@router.message(addTaskState.choosing_date, F.text)
async def add_choosing_date(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await message.answer("Введите описание задачи:", reply_markup=back_exit_kb)
        await state.set_state(addTaskState.choosing_desc.state)
        return
    elif message.text == 'Отмена':
        await state.clear()
        await message.answer("Создание задачи отменено!", reply_markup=ReplyKeyboardRemove())
        return

    try:
        date = datetime.strptime(message.text, '%d:%m:%Y')
    except ValueError:
        await message.answer('Проверьте правильность введенных данных в формате ДД:ММ:ГГГГ:',
                             reply_markup=back_exit_kb)
        await state.set_state(addTaskState.choosing_date.state)
        return

    data = await state.get_data()
    await state.update_data(expire=date)

    await message.answer(f"Проверьте введенные данные:\n"
                         f"Название: {data.get('title')}\n"
                         f"Описание: {data.get('description')}\n"
                         f"Выполнить до: {date.date()}",
                         reply_markup=confirm_back_exit_kb)

    await state.set_state(addTaskState.confirm.state)


@router.message(addTaskState.confirm, F.text)
async def add_confirm(message: Message, state: FSMContext, db: Database):
    if message.text == 'Назад':
        await message.answer("Введите дату до которой нужно выполнить задачу в формате ДД:ММ:ГГГГ:",
                             reply_markup=back_exit_kb)
        await state.set_state(addTaskState.choosing_date.state)

    elif message.text == 'Отмена':
        await state.clear()
        await message.answer("Создание задачи отменено!", reply_markup=ReplyKeyboardRemove())

    elif message.text == 'Подтвердить':
        data = await state.get_data()
        await db.add_task(data)
        await message.answer("Задача добавлена!", reply_markup=add_task_kb)
        await state.clear()

    else:
        await message.answer('Выберите из доступных кнопок!',
                             reply_markup=confirm_back_exit_kb)
        await state.set_state(addTaskState.confirm.state)



@router.message(F.text)
async def other(message: Message, ):
    await message.answer("Проверьте правильность введенной команды!\n"
                         "Используйте Помощь для получения доступных комманд!", reply_markup=add_task_kb)

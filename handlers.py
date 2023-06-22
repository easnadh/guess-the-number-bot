from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from utils import get_random_number, user


class FSMGame(StatesGroup):
    in_choice = State()
    start_game = State()
    game = State()


router = Router()


@router.message(Command('stats'))
async def end_game(message: types.Message):
    await message.answer(f'Всего игр: {user["total_games"]}\n'
                         f'Побед: {user["wins"]}')


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await message.answer(f'Давай сыграем в игру, {message.from_user.first_name}! '
                         f'Я загадаю число от 1 до 10, а ты попытаешься угадать.\n'
                         f'Напиши "go", чтобы сыграть или любое сообщение, чтобы отказаться.')
    await state.set_state(FSMGame.in_choice)


@router.message(FSMGame.in_choice)
async def start_game(message: types.Message, state: FSMContext):
    if message.text == 'go':
        user['secret_number'] = get_random_number()
        await message.answer(f'И так, как ты думаешь, что я загадал? Введи число.')
        user['attempts'] = 2
        await state.set_state(FSMGame.start_game)
    else:
        await message.answer(f'Когда захочешь сыграть, просто напиши "go".')
        await state.set_state(FSMGame.in_choice)


@router.message(FSMGame.start_game)
async def game(message: types.Message, state: FSMContext):
    await state.set_state(FSMGame.game)

    if user['attempts']:
        if int(message.text) == user['secret_number']:
            await message.answer(f"Верно, это {user['secret_number']}!")
            user['wins'] += 1
            await state.set_state(FSMGame.in_choice)
        else:
            user['attempts'] -= 1
            await message.answer(f'Попробуй еще раз')
            await state.set_state(FSMGame.start_game)
    else:
        await message.answer(f'Game over')
        await state.set_state(FSMGame.in_choice)

    user['total_games'] += 1


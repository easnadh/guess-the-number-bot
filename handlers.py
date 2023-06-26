from random import randint

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from db.requests.user_requests import get_user_attempts, get_user_stats, add_user_total_games, add_user_wins


class FSMGame(StatesGroup):
    game = State()


router = Router()


@router.message(Command('stats'))
async def get_stats(message: types.Message):
    games, wins = await get_user_stats(message.from_user.id)

    await message.answer(f'Всего игр: {games}\n'
                         f'Побед: {wins}')


@router.message(Command('start'))
async def start(message: types.Message):
    await message.answer(f'Давай сыграем в игру, {message.from_user.first_name}. '
                         f'Я загадаю число от 1 до 100, а ты попытаешься угадать.\n'
                         f'Напиши /game, чтобы сыграть. Напиши /stats, чтобы узнать свой счет.')


@router.message(Command('game'))
async def start_game(message: types.Message, state: FSMContext):
    await state.update_data(secret_number=randint(1, 100))
    await state.update_data(attempts=await get_user_attempts(message.from_user.id))

    await state.set_state(FSMGame.game)
    await message.answer(f'И так, как ты думаешь, что я загадал? Введи число.')


@router.message(FSMGame.game)
async def game(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    if int(message.text) != data['secret_number']:
        await state.update_data(attempts=data['attempts'] - 1)
        data = await state.get_data()
        await message.answer(f'Неверно. Оставшиеся попытки: {data["attempts"]}.')

        if data['attempts'] == 0:
            await add_user_total_games(message.from_user.id)
            await message.answer(f'Game over. Напиши /game, чтобы сыграть. Напиши /stats, чтобы узнать свой счет.')
            await state.clear()

    else:
        await message.answer(f"Верно, это {data['secret_number']}.")
        await add_user_wins(message.from_user.id)
        await add_user_total_games(message.from_user.id)
        await message.answer(f'Молодец! Напиши /game, чтобы сыграть. Напиши /stats, чтобы узнать свой счет.')

        await state.clear()

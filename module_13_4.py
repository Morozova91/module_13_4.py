# Задача "Цепочка вопросов":
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

api = ''
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Функция, обрабатывающая команду /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        'Привет! Я бот, помогающий твоему здоровью.')


# Функция для установки возраста
@dp.message_handler(text='Calories', state=None)
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


# Функция для установки роста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (в см):')
    await UserState.growth.set()


# Функция для установки веса
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес (в кг):')
    await UserState.weight.set()


# Функция для расчета и отправки нормы калорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)

    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    # Расчет по формуле Миффлина-Сан Жеора для мужчин
    calories = int(10 * weight + 6.25 * growth - 5 * age + 5)

    await message.answer(f"Ваша норма калорий: {calories} ккал в день")
    await state.finish()


if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)

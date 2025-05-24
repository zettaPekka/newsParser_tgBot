from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

from database.crud import create_user_if_not_exists, get_filter, set_filter
from parse import get_news
from keyboards.user_kbs import filters_kb, options_filters_kb, start_kb, regenerate_kb
from ai_regenerate import regenerate


user_router = Router()


def validate_filter(filter_name: str):
    output_filter = {
        'world': 'Политика',
        'economics': 'Экономика',
        'sport': 'Спорт',
        'culture': 'Культура',
        'science': 'Наука'
    }
    
    return output_filter.get(filter_name) if output_filter.get(filter_name) else 'Не указано'


@user_router.message(CommandStart())
async def start_handler(message: Message):
    await create_user_if_not_exists(message.from_user.id)
    await message.answer('<b>👋🏻 Добро пожаловать в новостной бот! Получайте актуальные новости на любую тему и перефразируйте их для публикации в вашем источнике. Просто введите команду /news и укажите тему, а я сделаю все остальное</b>',
                            reply_markup=start_kb)


@user_router.callback_query(F.data == 'start_get_news')
async def start_get_news_handler(callback: CallbackQuery):
    await callback.answer()
    
    filter_name = await get_filter(callback.from_user.id)
    filter_name = validate_filter(filter_name)

    await callback.message.edit_text(f'<b>Можете выбрать фильтр тематики новостей\nФильтр: {filter_name}</b>', 
                                        reply_markup=filters_kb)

@user_router.message(Command('news'))
async def news_handler(message: Message):
    filter_name = await get_filter(message.from_user.id)
    filter_name = validate_filter(filter_name)

    await message.answer(f'<b>Можете выбрать фильтр тематики новостей\nФильтр: {filter_name}</b>', 
                                        reply_markup=filters_kb)


@user_router.callback_query(F.data == 'get_news')
async def get_news_handler(callback: CallbackQuery):
    await callback.answer()
    waiting_message = await callback.message.answer('<b>Ожидайте...</b>')
    
    filter_name = await get_filter(callback.from_user.id)
    try:
        title, main_part, img_url = await get_news(rubric=filter_name)
    except:
        await callback.message.answer('<b>Не удалось получить новость, попробуйте еще раз</b>')
        return
    await callback.message.answer_photo(img_url, caption=f'<b>{title}</b>\n\n<i>{main_part}</i>',
                                    reply_markup=regenerate_kb)
    await waiting_message.delete()


@user_router.callback_query(F.data == 'back')
async def back_handler(callback: CallbackQuery):
    await callback.answer()
    filter_name = await get_filter(callback.from_user.id)
    filter_name = validate_filter(filter_name)

    await callback.message.edit_text(f'<b>Можете выбрать фильтр тематики новостей\nФильтр: {filter_name}</b>', 
                                        reply_markup=filters_kb)

@user_router.callback_query(F.data == 'regenerate')
async def regenerate_handler(callback: CallbackQuery):
    await callback.answer()
    waiting_message = await callback.message.answer('<b>Ожидайте...</b>')

    regenerated_text = await regenerate(callback.message.caption)
    try:
        await callback.message.edit_caption(str(callback.message.message_id), caption=regenerated_text, reply_markup=regenerate_kb)
    except:
        pass
    await waiting_message.delete()


@user_router.callback_query(F.data == 'filters')
async def filters_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('<b>Выберите тематику новостей</b>', reply_markup=options_filters_kb)


@user_router.callback_query(F.data.startswith('filter_'))
async def set_filter_handler(callback: CallbackQuery):
    await callback.answer()
    
    filter_name = callback.data.split('_')[1]
    
    if filter_name == 'reset':
        await set_filter(callback.from_user.id, None)
    else:
        await set_filter(callback.from_user.id, filter_name)
    
    filter_name = validate_filter(filter_name)
    await callback.message.edit_text(f'<b>Можете выбрать фильтр тематики новостей\nФильтр: {filter_name}</b>', 
                                        reply_markup=filters_kb)

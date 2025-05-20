from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


filters_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙️ Фильтры', callback_data='filters')],
    [InlineKeyboardButton(text='🗞 Получить новость', callback_data='get_news')]
])

options_filters_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Политика', callback_data='filter_world'),
        InlineKeyboardButton(text='Экономика', callback_data='filter_economics')],
    [InlineKeyboardButton(text='Спорт', callback_data='filter_sport'),
        InlineKeyboardButton(text='Культура', callback_data='filter_culture')],
    [InlineKeyboardButton(text='Наука', callback_data='filter_science'),
        InlineKeyboardButton(text='Сбросить', callback_data='filter_reset')],
    [InlineKeyboardButton(text='🔙 Вернуться', callback_data='back')]
])

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🗞 Получить новость', callback_data='start_get_news')]
])

regenerate_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Перефразировать (ИИ)', callback_data='regenerate')]
])
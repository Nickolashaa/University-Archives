from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.files.librarian import *


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📚Методички📚', callback_data='books')],
    [InlineKeyboardButton(text='📄Билеты📄', callback_data='tickets')]
])

books_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔎Поиск методички🔍', callback_data='search_book')],
    [InlineKeyboardButton(text='✏️Добавить методичку в архив✏️', callback_data='add_book')]
])

tickets_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔎Поиск билетов🔍', callback_data='search_tickets')],
    [InlineKeyboardButton(text='✏️Добавить билеты в архив✏️', callback_data='add_tickets')]
])


to_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🏠На главную🏠', callback_data='to_main')]
])


async def subjects_menu_book_read():
    builder = InlineKeyboardBuilder()
    for subject in get_book_subjects():
        builder.add(InlineKeyboardButton(text=f"✏️{subject}", callback_data=f"read_book_{subject}"))
    return builder.adjust(1).as_markup()


async def subjects_menu_tickets_read():
    builder = InlineKeyboardBuilder()
    for subject in get_tickets_subjects():
        builder.add(InlineKeyboardButton(text=f"✏️{subject}", callback_data=f"read_ticket_{subject}"))
    return builder.adjust(1).as_markup()


async def subjects_menu_book_write():
    builder = InlineKeyboardBuilder()
    for subject in get_book_subjects():
        builder.add(InlineKeyboardButton(text=f"✏️{subject}", callback_data=f"write_book{subject}"))
    builder.add(InlineKeyboardButton(text='Добавить Предмет', callback_data="add_book_subject"))
    return builder.adjust(1).as_markup()


async def subjects_menu_tickets_write():
    builder = InlineKeyboardBuilder()
    for subject in get_tickets_subjects():
        builder.add(InlineKeyboardButton(text=f"✏️{subject}", callback_data=f"write_ticket{subject}"))
    builder.add(InlineKeyboardButton(text='Добавить Предмет', callback_data="add_tickets_subject"))
    return builder.adjust(1).as_markup()
from aiogram import F, Bot, Dispatcher
from aiogram.enums import ChatAction
from aiogram.types import message, CallbackQuery, document
from aiogram.filters import CommandStart, Command
import app.keyboards as kb
from app.files.librarian import *
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from dotenv import load_dotenv
import os
from app.games.roll import rolling
from app.games.weird_game import SPERMA
load_dotenv()


start_text = "Приветствую! Я ваш проводник по архиву студентов!\n\nУ меня вы можете найти методички, билеты к предметам и многое другое!\n\nПо вопросам/предложениям писать @nick331045"
help_text = "Для запуска бота напишите /start или /arch\n\nБот интуитивно понятен, не понимаю, зачем вам инструкция???\n\nДля связи с автором напишите /nick"
rules_text = "1. Добавляйте только существующие предметы\n2. Добавляйте методички в формате .doc .docx .pdf\n3. Добавляя билеты,вы должны быть уверенными с достоверности информации + желательно в файле с билетами прописывать ответы на них"


bot = Bot(token=os.getenv('TOKEN_API'))
dp = Dispatcher()

last_subject = list()
last_chat_id = list()


def check(message_id):
    with open('app/files/stat.json', 'r') as f:
        stat = json.load(f)
        f.close()
    if message_id not in stat["id"]:
        stat["id"].append(message_id)
    stat["cnt"] += 1
    with open('app/files/stat.json', 'w') as f:
        json.dump(stat, f)
        f.close()


def admin(message):
    return message.chat.type == 'supergroup' and message.from_user.id == '841610537'


class NewSubjectBook(StatesGroup):
    subject = State()


class NewSubjectTickets(StatesGroup):
    subject = State()


class AddBook(StatesGroup):
    obj = State()


class AddTickets(StatesGroup):
    obj = State()


@dp.message(Command('arch'))
@dp.message(CommandStart())
async def cmd_start(message: message):
    last_chat_id.append(message.chat.id)
    check(message.chat.username)
    if len(last_chat_id) > 1000:
        last_chat_id.clear()
        last_chat_id.append(message.chat.id)
    await message.answer(start_text, reply_markup=kb.main)


@dp.callback_query(F.data == 'to_main')
async def callback_books(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(start_text, reply_markup=kb.main)


@dp.callback_query(F.data == 'books')
async def callback_books(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('📚Методички📚', reply_markup=kb.books_menu)


@dp.callback_query(F.data == 'tickets')
async def callback_books(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('📄Билеты📄', reply_markup=kb.tickets_menu)


@dp.callback_query(F.data == 'search_book')
async def callback_books(callback: CallbackQuery):
    await callback.answer('')
    if len(get_book_subjects()) != 0:
        await callback.message.edit_text('Выберите предмет...', reply_markup=await kb.subjects_menu_book_read())
    else:
        await callback.message.edit_text('Ни одной методички не было загружено :(', reply_markup=kb.to_main)


@dp.callback_query(F.data == 'search_tickets')
async def callback_books(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите предмет...', reply_markup=await kb.subjects_menu_tickets_read())


@dp.callback_query(F.data == 'add_book')
async def callback_books(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите предмет...', reply_markup=await kb.subjects_menu_book_write())


@dp.callback_query(F.data == 'add_tickets')
async def callback_books(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите предмет...', reply_markup=await kb.subjects_menu_tickets_write())


@dp.callback_query(F.data.contains('read_book'))
async def callback_books(callback: CallbackQuery):
    await callback.answer('')
    await bot.send_chat_action(last_chat_id[-1], ChatAction.TYPING)
    await callback.message.delete()
    for subject in get_book_subjects():
        if subject in callback.data:
            if len(get_book_items(subject)) == 0:
                await callback.message.answer('Файлов нет :(', reply_markup=kb.to_main)
            else:
                for item in get_book_items(subject):
                    file = FSInputFile(f"app/files/books/{item}")
                    await callback.message.answer_document(file)
                await callback.message.answer(f'Все методички по предмету {subject}✅', reply_markup=kb.to_main)


@dp.callback_query(F.data.contains('read_ticket'))
async def callback_books(callback: CallbackQuery):
    await callback.answer('')
    await bot.send_chat_action(last_chat_id[-1], ChatAction.TYPING)
    await callback.message.delete()
    for subject in get_tickets_subjects():
        if subject in callback.data:
            if len(get_tickets_items(subject)) == 0:
                await callback.message.answer('Файлов нет  :(', reply_markup=kb.to_main)
            else:
                for item in get_tickets_items(subject):
                    file = FSInputFile(f"app/files/tickets/{item}")
                    await callback.message.answer_document(file)
                await callback.message.answer(f'Все билеты по предмету {subject}✅', reply_markup=kb.to_main)


@dp.callback_query(F.data == 'add_book_subject')
async def callback_books(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewSubjectBook.subject)
    await callback.answer('')
    await callback.message.edit_text('Введите название предмета с заглавной буквы...')


@dp.message(NewSubjectBook.subject)
async def add_book_subject(message: message, state: FSMContext):
    await state.update_data(subject=message.text)
    data = await state.get_data()
    add_subject_book(data['subject'])
    await state.clear()
    await message.answer('✅Предмет успешно добавлен✅', reply_markup=kb.to_main)


@dp.callback_query(F.data == 'add_tickets_subject')
async def callback_books(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewSubjectTickets.subject)
    await callback.answer('')
    await callback.message.edit_text('Введите название предмета с заглавной буквы...')


@dp.message(NewSubjectTickets.subject)
async def add_book_subject(message: message, state: FSMContext):
    await state.update_data(subject=message.text)
    data = await state.get_data()
    add_subject_tickets(data['subject'])
    await state.clear()
    await message.answer('✅Предмет успешно добавлен✅', reply_markup=kb.to_main)


@dp.callback_query(F.data.contains('write_book'))
async def callback_add_book(callback: CallbackQuery, state: FSMContext):
    for subject in get_book_subjects():
        if subject in callback.data:
            last_subject.append(subject)
            break
    await state.set_state(AddBook.obj)
    await callback.answer('')
    await callback.message.edit_text('Отправьте методичку в формате doc, docx, pdf...')


@dp.message(AddBook.obj)
async def callback_add_book_3(message: document, state: FSMContext):
    await state.update_data(obj=message)
    add_book(last_subject[-1], message.document.file_name)
    last_subject.clear()
    document = message.document
    file_id = document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_file = await bot.download_file(file_path)
    file_name = document.file_name
    with open(f'app/files/books/{file_name}', 'wb') as new_file:
        new_file.write(downloaded_file.read())
        new_file.close()
    await message.answer('📚✅Добавление выполнено успешно', reply_markup=kb.to_main)
    await state.clear()


@dp.callback_query(F.data.contains('write_ticket'))
async def callback_add_book(callback: CallbackQuery, state: FSMContext):
    for subject in get_tickets_subjects():
        if subject in callback.data:
            last_subject.append(subject)
            break
    await state.set_state(AddTickets.obj)
    await callback.answer('')
    await callback.message.edit_text('Отправьте Билеты в формате doc, docx, pdf, напоминаю, что по правилам вы должны быть уверены в правильности билетов + желательно в файле должны быть ответы на них...')


@dp.message(AddTickets.obj)
async def callback_add_book_3(message: document, state: FSMContext):
    await state.update_data(obj=message)
    add_tickets(last_subject[-1], message.document.file_name)
    last_subject.clear()
    document = message.document
    file_id = document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_file = await bot.download_file(file_path)
    file_name = document.file_name
    with open(f'app/files/tickets/{file_name}', 'wb') as new_file:
        new_file.write(downloaded_file.read())
        new_file.close()
    await message.answer('📄✅Добавление выполнено успешно', reply_markup=kb.to_main)
    await state.clear()


@dp.message(Command('help'))
async def callback_add_book_3(message: message):
    await message.answer(help_text, reply_markup=kb.to_main)
    last_chat_id.append(message.chat.id)
    if len(last_chat_id) > 1000:
        last_chat_id.clear()
        last_chat_id.append(message.chat.id)


@dp.message(Command('rules'))
async def callback_add_book_3(message: message):
    await message.answer(rules_text, reply_markup=kb.to_main)
    last_chat_id.append(message.chat.id)
    if len(last_chat_id) > 1000:
        last_chat_id.clear()
        last_chat_id.append(message.chat.id)


@dp.message(Command('nick'))
async def callback_add_book_3(message: message):
    await message.answer("Автор бота: @nick331045", reply_markup=kb.to_main)
    last_chat_id.append(message.chat.id)
    if len(last_chat_id) > 1000:
        last_chat_id.clear()
        last_chat_id.append(message.chat.id)


@dp.message(F.text == "Бот.Статистика")
async def callback_add_book_3(message: message):
    with open('app/files/stat.json', 'r') as f:
        stat = json.load(f)
        f.close()
    cnt = stat["cnt"]
    await message.answer(f"Всего ботом пользовались {cnt} раз")


@dp.message(F.text == "Бот.Список")
async def callback_add_book_3(message: message):
    with open('app/files/stat.json', 'r') as f:
        stat = json.load(f)
        f.close()
    await message.answer("Полный список пользователей, которые пользовались ботом")
    for item in stat["id"]:
        await message.answer(f"@{item}")


@dp.message(Command('game_words'))
async def game_words(message:message):
    if admin(message):
        await message.answer("Начинаем игру в слова\nСледующее слово начинается на последнюю букву предыдущего\nПовторяться слова не должны")


@dp.message(Command('roll'))
async def test(message:message):
    res = rolling(message.from_user.first_name)
    if res == 0:
        await message.reply(f"Увы, {message.from_user.first_name}, отныне ты жертва Носовицкого")
    else:
        await message.reply(f"Повезло, {message.from_user.first_name} не стал попуском {res} раз")


@dp.message(Command('SPERMA'))
async def test(message:message):
    res = SPERMA(message.from_user.first_name)
    await message.reply(f"{message.from_user.first_name} сверкнул умом {res} раз")
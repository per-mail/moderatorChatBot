#video https://www.youtube.com/watch?v=MEj4J0y4GwU&list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ&index=5&t=387s
from aiogram import types, executor,  Dispatcher
from create import dp, bot, conn, cur, GROUP_ID, OWNER_ID, BOT_ID
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.dispatcher import FSMContext


from aiogram.types.chat_permissions import ChatPermissions
from admins_filter import moderators, ADMINS_LIST

class dialog(StatesGroup):
    spam = State()
    blacklist = State()
    whitelist = State()
    admin_in = State()
    admin_out = State()


#@dp.message_handler(state='*', text='Назад')
async def back(message: Message):
# проверяем на право доступа     
# получаем список админов 2 способ, мой с функцией
    moderators() 
    if message.from_user.id in ADMINS_LIST:  
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
        await message.answer('Основное меню', reply_markup=keyboard)
    else:
        await message.answer(f'{message.from_user.first_name}. Вам не доступна эта функция')



#@dp.message_handler(content_types=['text'], text='Рассылка')
async def spam(message: Message):
#проверяем есть ли пользователь в списке админов
# получаем список админов 2 способ, мой с функцией
    moderators() 
    if message.from_user.id in ADMINS_LIST:    
        await dialog.spam.set()        
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад"))        
        await message.answer(f'{message.from_user.first_name} напиши текст рассылки или нажми кнопку назад', reply_markup=keyboard)
    else:   
        await message.answer(f'{message.from_user.first_name}. Вы не являетесь администратором чата')
        
#Здесь и далее берём user_id из message.text из текста сообщения или из текста который приходит из базы.      

#@dp.message_handler(state=dialog.spam)
async def start_spam(message: Message, state: FSMContext):
    if message.text != 'Назад':
        cur = conn.cursor()
        cur.execute(f"SELECT user_id FROM users WHERE admin = 'False'")
        #cur.execute(f'SELECT user_id FROM users')
        spam_base = cur.fetchall()
        print(spam_base)
        for q in range(len(spam_base)):
           print(spam_base[q][0])
        for q in range(len(spam_base)):
           await bot.send_message(spam_base[q][0], message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
        await message.answer(f'{message.from_user.first_name}. Рассылка завершена', reply_markup=keyboard)
        await state.finish()
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
        keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
        keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
        await message.answer(f'{message.from_user.first_name}. Рассылка остановлена', reply_markup=keyboard)
    pass
        
    


#@dp.message_handler(content_types=['text'], text='Добавить в ЧС')
async def hanadler(message: types.Message, state: FSMContext):
# проверяем на право доступа     
# получаем список админов 2 способ, мой с функцией
    moderators()
    if message.from_user.id in ADMINS_LIST: 
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад"))
        await message.answer(
            f'{message.from_user.first_name}. Введите id пользователя, которого нужно заблокировать или нажми кнопку назад',
            reply_markup=keyboard)
#подключаемся к базе
        await dialog.blacklist.set()
    else:   
        await message.answer(f'{message.from_user.first_name}. Вы не являетесь администратором чата') 


#@dp.message_handler(state=dialog.blacklist)
async def proce(message: types.Message, state: FSMContext):
    if message.text.isdigit() and message.text != 'Назад':# проверяем что все символы цифры
            cur = conn.cursor()
            cur.execute(f'SELECT block FROM users WHERE user_id = {message.text}') #берём user_id из message.text и ищём есть ли он в базе
            result = cur.fetchall()
            conn.commit()
            if len(result) == 0:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=keyboard)
                await state.finish()
            else:
                a = result[0] # здесь мы избавляемся от запятой
                d = a[0]                
                if d == 'False':
                    cur.execute(f"UPDATE users SET block = 'True' WHERE user_id = {message.text}")
                    conn.commit()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer(f'Пользователь успешно добавлен в ЧС.', reply_markup=keyboard)
                    await state.finish()
                    #вводим ограничения на пользователя
                    await bot.restrict_chat_member(GROUP_ID, message.text)#берём user_id из message.text
                    await bot.send_message(message.text, 'Администратор добавил Вас в чёрный список!')                    
                else:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer('Данный пользователь уже получил бан', reply_markup=keyboard)
                    #вводим ограничения на пользователя
                    await bot.restrict_chat_member(chat_id=GROUP_ID, user_id=message.text)#берём user_id из message.text
                    await bot.send_message(message.text, 'Вы получили ограничения')
                    await state.finish()
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад"))        
        await message.answer(f'{message.from_user.first_name} Ты вводишь буквы введи ID пользователя или нажми кнопку назад', reply_markup=keyboard)
        pass
       
        

        

#@dp.message_handler(content_types=['text'], text='Убрать из ЧС')
async def hfandler(message: types.Message, state: FSMContext):
# проверяем на право доступа     
# получаем список админов 2 способ, мой с функцией
    moderators()    
    if message.from_user.id in ADMINS_LIST:   
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Назад"))
            await message.answer(
                f'{message.from_user.first_name}. Введите id пользователя, которого нужно разблокировать или нажми кнопку назад',
                reply_markup=keyboard)
            await dialog.whitelist.set()
    else:   
        await message.answer(f'{message.from_user.first_name}. Вы не являетесь администратором чата')


#@dp.message_handler(state=dialog.whitelist)
async def proc(message: types.Message, state: FSMContext):
    if message.text.isdigit():
            cur = conn.cursor()
            cur.execute(f'SELECT block FROM users WHERE user_id = {message.text}')
            result = cur.fetchall()
            conn.commit()
            if len(result) == 0:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=keyboard)
                await state.finish()
            else:
                a = result[0] # здесь мы избавляемся от запятой  
                d = a[0]
                if d == 'True':
                    cur = conn.cursor()
                    cur.execute(f"UPDATE users SET block = 'False' WHERE user_id = {message.text}")
                    conn.commit()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в списка админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer('Пользователь успешно разбанен.', reply_markup=keyboard)
                    await state.finish()
                    #берём user_id из message.text
                    await bot.restrict_chat_member(GROUP_ID, message.text,ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True,
                        can_add_web_page_previews=True))
                    await bot.send_message(message.text, 'Вы были разблокированы администрацией.')
                else:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer(f'{message.from_user.first_name}. не получал бан.', reply_markup=keyboard)
                    await state.finish()
    else:
          keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
          keyboard.add(types.InlineKeyboardButton(text="Назад"))        
          await message.answer(f'{message.from_user.first_name} Ты вводишь буквы введи ID пользователя или нажми кнопку назад', reply_markup=keyboard)





          

async def admin_in(message: types.Message, state: FSMContext):
# проверяем на право доступа     
# получаем список админов 2 способ, мой с функцией
    moderators()    
    if message.from_user.id in ADMINS_LIST: 
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад"))
        await message.answer(
            f'{message.from_user.first_name}. Введите id пользователя, которого нужно добавить в список или нажми кнопку назад',
            reply_markup=keyboard)
#подключаемся к базе
        await dialog.admin_in.set()
    else:   
        await message.answer(f'{message.from_user.first_name}. Вы не являетесь администратором чата')
        


#@dp.message_handler(state=dialog.blacklist)
async def adminin(message: types.Message, state: FSMContext):     
        if message.text.isdigit():# проверяем что все символы цифры
            cur = conn.cursor()
            cur.execute(f'SELECT admin FROM users WHERE user_id = {message.text}') #берём user_id из message.text и ищём есть ли он в базе
            result = cur.fetchall()
            conn.commit()
            if len(result) == 0:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=keyboard)
                await state.finish()
            else:
                a = result[0] # здесь мы избавляемся от запятой
                d = a[0]                
                if d == 'False':
                    cur.execute(f"UPDATE users SET admin = 'True' WHERE user_id = {message.text}")
                    conn.commit()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer(f'Пользователь успешно добавлен в список админов.', reply_markup=keyboard)
                    ADMINS_LIST.append(message.text)                    
                    await state.finish()
                   
                    await bot.send_message(message.text, 'Администратор добавил Вас в список админов!')                    
                else:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer('Данный пользователь уже есть списке админов!', reply_markup=keyboard)
                    await state.finish()
        else:
            await message.answer(f'{message.from_user.first_name}. Ты вводишь буквы.')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Назад"))        
            await message.answer(f'{message.from_user.first_name} Ты вводишь буквы введи ID пользователя или нажми кнопку назад', reply_markup=keyboard)



#@dp.message_handler(content_types=['text'], text='Убрать из списка\n админов')
async def admin_out(message: types.Message, state: FSMContext):
# проверяем на право доступа     
# получаем список админов 2 способ, мой с функцией
    moderators()    
    if message.from_user.id in ADMINS_LIST:   
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Назад"))
            await message.answer(
                f'{message.from_user.first_name}. Введите id пользователя, которого нужно убрать из списка админов или нажми кнопку назад',
                reply_markup=keyboard)
            await dialog.admin_out.set()
    else:   
        await message.answer(f'{message.from_user.first_name}. Вы не являетесь администратором чата')



async def adminout(message: types.Message, state: FSMContext):
    if message.text.isdigit():
            cur = conn.cursor()
            cur.execute(f'SELECT admin FROM users WHERE user_id = {message.text}')
            result = cur.fetchall()
            conn.commit()
            if len(result) == 0:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=keyboard)
                await state.finish()
            else:
                a = result[0] # здесь мы избавляемся от запятой  
                d = a[0]
                if d == 'True':
                    cur = conn.cursor()
                    cur.execute(f"UPDATE users SET admin = 'False' WHERE user_id = {message.text}")
                    conn.commit()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer('Пользователь успешно удалён из списка админов', reply_markup=keyboard)
                    await state.finish()
                    await bot.send_message(message.text, 'Вы были удалены из списка админов')
                else:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(types.InlineKeyboardButton(text="Рассылка"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из ЧС"))
                    keyboard.add(types.InlineKeyboardButton(text="Добавить в список админов"))
                    keyboard.add(types.InlineKeyboardButton(text="Убрать из списка админов"))
                    await message.answer(f'{message.from_user.first_name}.нет в списке админов.', reply_markup=keyboard)
                    await state.finish()
    else:
          await message.answer(f'{message.from_user.first_name}. Ты вводишь буквы...')
          keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
          keyboard.add(types.InlineKeyboardButton(text="Назад"))        
          await message.answer(f'{message.from_user.first_name} Ты вводишь буквы введи ID пользователя или нажми кнопку назад', reply_markup=keyboard)

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(spam, content_types=['text'], text='Рассылка')
    dp.register_message_handler(start_spam, state=dialog.spam)
    dp.register_message_handler(back, state='*', text='Назад')
    dp.register_message_handler(hanadler, content_types=['text'], text='Добавить в ЧС')
    dp.register_message_handler(proce, state=dialog.blacklist)
    dp.register_message_handler(hfandler, content_types=['text'], text='Убрать из ЧС')
    dp.register_message_handler(proc, state=dialog.whitelist)
    
    dp.register_message_handler(admin_in, content_types=['text'], text='Добавить в список админов')
    dp.register_message_handler(adminin, state=dialog.admin_in)
    dp.register_message_handler(admin_out, content_types=['text'], text='Убрать из списка админов')
    dp.register_message_handler(adminout, state=dialog.admin_out)
    
    

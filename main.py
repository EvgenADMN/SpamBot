import time
import asyncio
import telebot


class L_kitchen_bot:
    def __init__(self):
        self.token = '1111111:AAAA-AAAAAAAAAAA-AAAAAAAAAA'
        self.bot = telebot.TeleBot(self.token)
        self.whitelist = {
            111111111: 'evgen',
            222222222: 'neevgen'
        }
        self.sendlist = {v: k for k, v in self.whitelist.items()}
        self.floodlist = {
            -123321123321: 'test',
        }

    def run(self):
        def set_floodstate(value):
            with open('states/flood', 'w', encoding='UTF8') as file:
                file.write(str(value))


        def set_message_state(state):
            with open('states/message', 'w', encoding='UTF8') as file:
                file.write(str(state))


        def set_interval_state(value):
            with open('states/interval', 'w', encoding='UTF8') as file:
                file.write(str(value))


        def floodstate():
            with open('states/flood', encoding='UTF8') as file:
                state = int(file.read())
                return state

        def message_state():
            with open('states/message', encoding='UTF8') as file:
                state = int(file.read())
                return state

        def interval_state():
            with open('states/interval', encoding='UTF8') as file:
                state = int(file.read())
                return state

        def read_message():
            with open('message', encoding='UTF8') as file:
                state = file.read()
                return state

        def read_interval():
            with open('interval', encoding='UTF8') as file:
                state = int(file.read())
                return state

        def admin_page():
            set_message_state(0)
            set_interval_state(0)
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            if floodstate():
                spam_button = '🟢 Рассылка'
            else:
                spam_button = '⚫️ Рассылка'

            buttons = (spam_button, '💌 Сообщение', '🕔 Интервал')
            for button in buttons:
                markup.add(button)

            return markup


        def message_menu(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            set_message_state(1)
            markup.add('◀️Вернуться в меню')
            self.bot.send_message(message.chat.id, 'Отправь сообщение для рассылки ответным письмом', reply_markup=markup)


        def interval_menu(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            set_interval_state(1)
            markup.add('◀️Вернуться в меню')
            self.bot.send_message(message.chat.id, 'Отправь интервал в секундах(!)',
                                  reply_markup=markup)


        def back_to_menu(message):
            markup = admin_page()
            set_message_state(0)
            set_interval_state(0)
            self.bot.send_message(message.chat.id, 'Главное меню',
                                  reply_markup=markup)


        async def flood(message, interval):
            while True:
                if floodstate():
                    for group in self.floodlist:
                        self.bot.send_message(group, message)
                    time.sleep(interval)
                else:
                    break



        messages = {
            '💌 Сообщение': message_menu,
            '🕔 Интервал': interval_menu,
            '◀️Вернуться в меню': back_to_menu,
        }

        set_floodstate(0)
        set_interval_state(0)
        set_message_state(0)


        @self.bot.message_handler(commands=['start', 'run', 'zavodis'])
        def start_message(message):
            markup = admin_page()
            if message.chat.id in self.whitelist:
                self.bot.send_message(message.chat.id, 'Привет, хозяин', reply_markup=markup)
            else:
                self.bot.send_message(message.chat.id, 'Добрый день! Какой у вас вопрос?')


        @self.bot.message_handler(content_types='text')
        def message_handler(message):
            if message.chat.id in self.whitelist:
                if message.text == '⚫️ Рассылка':
                    set_floodstate(1)
                    markup = admin_page()
                    self.bot.send_message(message.chat.id, 'Привет, хозяин', reply_markup=markup)
                    asyncio.run(flood(read_message(), read_interval()))

                elif message.text == '🟢 Рассылка':
                    set_floodstate(0)
                    markup = admin_page()
                    self.bot.send_message(message.chat.id, 'Привет, хозяин', reply_markup=markup)
                else:
                    if message_state() and message.text not in messages:
                        with open('message', 'w', encoding='UTF8') as file:
                            file.write(message.text)
                        self.bot.send_message(message.chat.id, 'Сообщение установлено', reply_markup=admin_page())
                    elif interval_state() and message.text not in messages:
                        try:
                            int(message.text)
                            with open('interval', 'w', encoding='UTF8') as file:
                                file.write(message.text)
                            self.bot.send_message(message.chat.id, 'Интервал установлен', reply_markup=admin_page())
                        except:
                            self.bot.send_message(message.chat.id, 'Нормальный интервал установи')
                    else:
                        try:
                            messages[message.text](message)
                        except:
                            pass
            else:
                self.bot.forward_message(self.sendlist['neevgen'], message.chat.id, message.message_id)

        self.bot.polling(interval=0)


if __name__ == '__main__':
    while True:
        try:
            bot = L_kitchen_bot()
            bot.run()
        except:
            time.sleep(5)
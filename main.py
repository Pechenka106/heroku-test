import telebot
from telebot import types
from requests import get
from emoji import *
import datetime as dt
import random
import os

path = 'C:\\Users\\SER\\PycharmProjects\\test'
commands = {'/start': 'Приветствие',
            '/help': 'Вывод всех команд бота и их функционал',
            '/images': 'Получить случайную картинку выбранного животного',
            '/music': 'Получить случайную песню из выбранного жанра'}


bot = telebot.TeleBot(open(f'{path}\\token.txt', 'r').readline())


def write_log(user, message='DEBUG'):
    log = open(f'{path}\\log.txt', 'w')
    log.write(f'{dt.datetime.now()}: Пользователь - {user.id}({user.first_name} '
              f'{user.last_name}) *** {message}')
    log.close()


@bot.message_handler(commands=['start'])
def start(msg):
    if msg.id == 1:
        write_log(msg.from_user, 'Начала общение с Дженифер')
    write_log(msg.from_user, 'Поздоровался')
    bot.send_message(msg.chat.id, f'Привет, <b>{msg.from_user.first_name} {msg.from_user.last_name}</b>.'
                                  f' Я рада тебя видеть. Введи "/help" чтобы узнать мои возможости.', parse_mode='html')


@bot.message_handler(commands=['help'])
def show_command(msg):
    # bot.send_message(msg.chat.id, str(msg)),
    bot.send_message(msg.chat.id, 'Вот список моих умений:\n' +
                     '\n'.join([f'{key} – {commands[key]}' for key in commands.keys()]))


@bot.message_handler(commands=['images'])
def get_message(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    [markup.add(types.KeyboardButton(item)) for item in ['Котики 🐱', 'Собачки 🐶', 'Лисички 🦊', 'Стоп 🚫']]
    bot.send_message(msg.chat.id, 'Выберите что вы хотите увидеть', reply_markup=markup)


@bot.message_handler(commands=['music'])
def phonk(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    [markup.add(types.KeyboardButton(item)) for item in ['Phonk', 'Стоп 🚫']]
    bot.send_message(msg.chat.id, 'Выбери что ты хочешь послушать', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_photo(msg):
    if msg.text.lower() == 'котики 🐱':
        bot.send_message(msg.chat.id, 'Секундочку ⏳')
        photo = open(f'{path}\\photo\\cat.jpg', 'wb')
        url = get(get('https://aws.random.cat/meow').json()['file']).content
        photo.write(url)
        photo.close()
        bot.send_photo(msg.chat.id, open(f'{path}\\photo\\cat.jpg', 'rb'), 'Воть 😁')
    elif msg.text.lower() == 'собачки 🐶':
        bot.send_message(msg.chat.id, 'Секундочку ⏳')
        photo = open(f'{path}\\photo\\dog.jpg', 'wb')
        url = get(get('https://random.dog/woof.json').json()['url']).content
        photo.write(url)
        photo.close()
        bot.send_photo(msg.chat.id, open(f'{path}\\photo\\dog.jpg', 'rb'), 'Воть 😁')
    elif msg.text.lower() == 'лисички 🦊':
        bot.send_message(msg.chat.id, 'Секундочку ⏳')
        photo = open(f'{path}\\photo\\fox.jpg', 'wb')
        url = get(get('https://randomfox.ca/floof/').json()['image']).content
        photo.write(url)
        photo.close()
        bot.send_photo(msg.chat.id, open(f'{path}\\photo\\fox.jpg', 'rb'), 'Воть 😁')
    elif msg.text.lower() == 'стоп 🚫':
        bot.send_message(msg.chat.id, 'Похоже хватит на сегодня картиночек)',
                         reply_markup=types.ReplyKeyboardRemove())
    elif msg.text.lower() == 'phonk':
        bot.send_message(msg.chat.id, 'Секундочку ⏳')
        directory = f'{path}\\music\\phonk'
        music = open(directory + '\\' + random.choice(os.listdir(directory)), 'rb')
        bot.send_audio(msg.chat.id, music)


bot.infinity_polling(timeout=1)

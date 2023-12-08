import csv
import os
import random

import requests
import telebot
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Привет, ты написал мне /start или /help.\n"
                                      "Используй /todos для получения рандомной цитаты, /comments для получения рандомного комментария или /posts для получения рандомного поста.")

@bot.message_handler(commands=['posts'])
def handle_quote(message):
    url = f"https://jsonplaceholder.typicode.com/posts/{random.randint(1, 200)}"
    response = requests.get(url)
    if response.status_code == 200:
        posts = response.json()
        idx = posts['id']
        title = posts['title']
        body = posts['body']
        bot.send_message(message.chat.id, f"Заголовок: {posts['title']}\nТекст: {posts['body']}")
        with open('posts.csv', 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'Заголовок', 'Текст']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow({
                'id': idx,
                'Заголовок': title,
                'Текст': body,
            })
    else:
        bot.send_message(message.chat.id, "Данные не найдены")


@bot.message_handler(commands=['comments'])
def handle_quote(message):
    url = f"https://jsonplaceholder.typicode.com/comments/{random.randint(1, 200)}"
    response = requests.get(url)
    if response.status_code == 200:
        comments = response.json()
        idx = comments['id']
        name = comments['name']
        email = comments['email']
        body = comments['body']
        bot.send_message(message.chat.id, f"Имя: {comments['name']}\nEmail: {comments['email']}\nТекст: {comments['body']}")
        with open('comments.csv', 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'Имя', 'Email', 'Текст']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow({
                'id': idx,
                'Имя': name,
                'Email': email,
                'Текст': body,
            })
    else:
        bot.send_message(message.chat.id, "Данные не найдены")

@bot.message_handler(commands=['todos'])
def handle_quote(message):
    url = f"https://jsonplaceholder.typicode.com/todos/{random.randint(1, 200)}"
    response = requests.get(url)
    if response.status_code == 200:
        todos = response.json()
        idx = todos['id']
        title = todos['title']
        userid = todos['userId']
        if bool(todos['completed']):
            completed = 'Выполнено'
        else:
            completed = 'Не выполнено'
        bot.send_message(message.chat.id, f"Задача: {todos['title']}\nСтатус: {completed}")
        with open('todos.csv', 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'Заголовок', 'Пользователь', 'Статус']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow({
                'id': idx,
                'Заголовок': title,
                'Пользователь': userid,
                'Статус': completed,
            })
    else:
        bot.send_message(message.chat.id, "Задача не найдена")

bot.polling(none_stop=True)

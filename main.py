from flask import Flask, render_template, request
import mysql.connector

from flask import Flask, render_template, request

import dbModule as db

app = Flask(__name__)

'''
обработчик от страницы создания статьи, получает из полей ввода строки и загружает в бд
'''
@app.route('/', methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        text = request.form.get('text')

        db.add_new_article(title, subtitle, text)
    return render_template('index.html')

'''
обработчик от страницы поиска статьи, получает строку из поля ввода, если она состоит из букв - поиск по 
вхождению фразы в заголовок, если из цифр - поиск по id
'''
@app.route('/find', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        data = request.form.get('data')
        if data.isalpha():
            return db.find_by_substring_in_title(data)
        elif data.isdigit():
            return db.find_by_id(data)


    return render_template('find.html')

if __name__ == "__main__":
    app.run()
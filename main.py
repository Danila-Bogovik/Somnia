# from flask import Flask, render_template, request, Response
# import mysql.connector
#
# app = Flask(__name__)
#
#
# import dbModule as db
#
#
# with open('Cat2.jpg', 'br') as f:
#     db.add_picture(f.read(), 'cat', 'image/jpeg')
#
#
#
#
#
# @app.route("/", methods=["GET", "POST"])
# def index():
#     picture_data = db.find_picture_by_name('cat')
#
#     return Response(picture_data[1], content_type=picture_data[3])
#
# if __name__ == "__main__":
#     app.run()
#
#
#
from flask import Flask, render_template, request
import mysql.connector

from flask import Flask, render_template, request

import dbModule as db

application = Flask(__name__)

'''
обработчик от страницы создания статьи, получает из полей ввода строки и загружает в бд
'''
@application.route('/', methods=['GET', 'POST'])
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
@application.route('/find', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        data = request.form.get('data')
        if data.isalpha():
            return db.find_by_substring_in_title(data)
        elif data.isdigit():
            return db.find_by_id(data)


    return render_template('find.html')

if __name__ == "__main__":
    application.run(host='0.0.0.0')
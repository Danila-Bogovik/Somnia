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
import flask
import mysql.connector
import json
from werkzeug.utils import secure_filename
import os

from flask import Flask, render_template, request

import dbModule as db

application = Flask(__name__)
application.config['ALLOWED_EXTENSIONS'] = {'html'}
application.config['UPLOAD_FOLDER'] = 'uploads/'
print(db.get_data_for_search_by_substrinng('ti', 2, 1))

'''
обработчик от страницы создания статьи, получает из полей ввода строки и загружает в бд
'''

html_content = ""

@application.route('/', methods=['GET', 'POST'])
def page0():
    return render_template('index.html')

@application.route('/upload', methods=['GET', 'POST'])
def page1():
    # if request.method == 'POST':
    #     title = request.form.get('title')
    #     subtitle = request.form.get('subtitle')
    #     text = request.form.get('text')
    #
    #     db.add_new_article(title, subtitle, text)
    # return render_template('index.html')

    if 'file' not in request.files:
        return 'Нет части файла', 400 # Bad request
    file = request.files['file']
    if file.filename == '':
        return 'Никакой файл не выбран', 400 # Bad request
    if file and file.filename.endswith('.html'):
        global html_content
        html_content = file.read().decode() # читаем файл и переводим в строковую переменную
        db.add_new_article("Заголовок", "Описание", html_content)
        return 'Содержимое файла успешно сохранено в переменную', 200 # OK
    return 'Неправильный файл', 400 # Bad request

'''
обработчик от страницы поиска статьи, получает строку из поля ввода, если она состоит из букв - поиск по 
вхождению фразы в заголовок, если из цифр - поиск по id
'''


# @application.route('/find', methods=['GET', 'POST'])
# def page2():
#     if request.method == 'POST':
#         data = request.form.get('data')
#         if data.isalpha():
#             return db.find_by_substring_in_title(data)
#         elif data.isdigit():
#             return db.find_by_id(data)
#
#     return render_template('find.html')


@application.route('/search', methods=['GET', 'POST'])
def page3():
    return render_template('search.html')


@application.route('/search?substring=<substring>', methods=['GET', 'POST'])
def page4():
    if request.method == 'POST':
        data = request.form.get('data')
        if data.isalpha():
            res = {}
            d = db.get_data_for_search_by_substrinng(data, 10, 10)
            for i in range(len(d)):
                res[i+1] = d[i]
            return flask.jsonify(res)

        elif data.isdigit():
            return db.find_by_id(data)

    return render_template('search.html')



if __name__ == "__main__":
    application.run(host='0.0.0.0')




























    
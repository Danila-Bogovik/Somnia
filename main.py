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



from flask import Flask, app, render_template, request, Response, jsonify
import bleach
from flask import Flask, render_template, request
import dbModule as db

import linksGenerator as lg
import Utils

application = Flask(__name__)

page_width = 10

# title = 'Бедный девопс'
#
# db.add_new_article(title, 'Эх, бедолага!', '<b>Сегодня, с утра и до вечера, бедолага девопс не мог оживить умерший сайт...</b>')
#
# article_id = db.get_data_for_search_by_substrinng(title, 1, 0)[0][0]
#
# link = lg.create_link(title, 21, 10)
#
# db.add_link_to_article(link, article_id)
#
# print(db.get_link_by_id(article_id))
# print(db.get_id_by_link(link))


'''
обработчик от страницы создания статьи, получает из полей ввода строки и загружает в бд
'''

@application.route('/', methods=['GET', 'POST'])
def page0():
    if request.method == 'POST':
        title = bleach.clear(request.form.get('title'))
        subtitle = bleach.clear(request.form.get('subtitle'))
        text = bleach.clear(request.form.get('text'))

        db.add_new_article(title, subtitle, text)
    return render_template('index.html')

# @application.route('/add_article', methods=['GET', 'POST'])
# def page1():
#     if request.method == 'POST':
#         title = bleach.clear(request.form.get('title'))
#         subtitle = bleach.clear(request.form.get('subtitle'))
#         text = bleach.clear(request.form.get('text'))
#
#
#
#         db.add_new_article(title, subtitle, text)
#     return render_template('index.html')

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



@application.route('/search-page',  methods=['GET', 'POST'])
def get_search_page():
    return render_template('search-articles.html')

@application.route('/search', methods=['GET', 'POST'])
def search_articles_with_substring():
    substring = request.args.get('s')  # s - Подстрока
    page_index = request.args.get('i')  # i - индекс текущей страницы.

    if not substring or not page_index:
        data = None
    else:
        data = db.get_data_for_search_by_substrinng(substring, page_width, page_width * int(page_index))

    if data is None:
        return Response('Not found!', content_type='text/html')
    else:
        json_data = {}
        for item in data:
            item_id = item[0]
            title = item[1]
            subtitle = item[2]
            date = item[3]
            json_data[item_id] = {
                'title': title,
                'subtitle': subtitle,
                'date': date
            }

        return jsonify(json_data)



if __name__ == "__main__":
    application.run(host='0.0.0.0')







    
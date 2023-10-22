from flask import Flask, app, render_template, request, Response, jsonify
import linksGenerator as lg
import dbModule as db
import Utils
import os

application = Flask(__name__)
page_width = 10

'''
обработчик от страницы создания статьи, получает из полей ввода строки и загружает в бд
'''
@application.route('/', methods=['GET', 'POST'])
def page0():
    return render_template('index.html')

@application.route('/add_articles', methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        text = request.form.get('text')

        db.add_new_article(title, subtitle, text)
    return render_template('index.html')

@application.route('/add_picture', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        image = request.files['image']
        print(image)
        if image:
            filename = image.filename    # this is for security purposes
            image.save(filename)                         # save the image in the server (this is optional, you can directly read the bytes)
            with open(filename, 'rb') as f:
                picture_bytes = f.read()
            os.remove(filename)                          # remove the image file from server

            image_name = image.filename
            image_type = os.path.splitext(image_name)[1]

            try:
                db.add_picture(picture_bytes, image_name, image_type)
                return {"status": "success", "message": "Image uploaded successfully"}
            except Exception as e:
                return {"status": "failure", "message": str(e)}

        else:
            return {"status": "failure", "message": "No image found in the request"}

    return render_template('index.html')

'''
обработчик от страницы поиска статьи, получает строку из поля ввода, если она состоит из букв - поиск по 
вхождению фразы в заголовок, если из цифр - поиск по id
'''
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
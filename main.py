from flask import Flask, render_template, request
import mysql.connector

from flask import Flask, render_template, request

import dbModule as db

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        text = request.form.get('text')

        db.add_new_article(title, subtitle, text)
        return 'Успешно сохранено!', 200
    return render_template('page1.html')

@app.route('/find', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        data = request.form.get('data')
        if data.isalpha():
            db.find_by_substring_in_title(data)
        elif data.isdigit():
            db.find_by_id(data)

        return 'Успешно сохранено!', 200
    return render_template('page2.html')

if __name__ == "__main__":
    app.run()
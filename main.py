from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


import dbModule as db

with open("cat2.jpg", "rb") as f:
    image_data = f.read()

db.add_new_article('another title', 'lol', 'heh')

print(db.find_by_substring_in_title('some'))

print(db.find_picture_by_name('cat'))



@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        return "Файл успешно загружен и сохранен в базу данных!"

    return 'hello'

if __name__ == "__main__":
    app.run()
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


import dbModule as db

print(db.find_by_substring_in_title('some'))



@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        return "Файл успешно загружен и сохранен в базу данных!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run()
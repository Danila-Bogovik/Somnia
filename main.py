from flask import Flask, render_template, request, Response
import mysql.connector

app = Flask(__name__)


import dbModule as db


with open('Cat2.jpg', 'br') as f:
    db.add_picture(f.read(), 'cat', 'image/jpeg')
    




@app.route("/", methods=["GET", "POST"])
def index():
    picture_data = db.find_picture_by_name('cat')

    return Response(picture_data[1], content_type=picture_data[3])

if __name__ == "__main__":
    app.run()
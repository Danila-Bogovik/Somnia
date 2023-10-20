from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Настройка соединения с базой данных MySQL
db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="yourdatabase"
)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = file.filename
        filedata = file.read()

        cursor = db.cursor()
        cursor.execute("INSERT INTO files (filename, filedata) VALUES (%s, %s)", (filename, filedata))
        db.commit()

        return "Файл успешно загружен и сохранен в базу данных!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run()
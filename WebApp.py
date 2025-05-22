import os
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD"] = UPLOAD_FOLDER
app.secret_key = "sUpeR_SecRet"

users = {
    "Asad": "1234",
    "Jochen": "python",
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")

@app.route("/file-upload")
def file_upload():
    return render_template("image.html")

@app.route("/handle-login", methods=["POST"])
def handle_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            return render_template("homepage.html")
        else:
            return render_template("error_login.html")
    return render_template("index.html")

@app.route("/handle-calc-request", methods=["POST"])
def handle_calc_request():
    if request.method == "POST":
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operation = request.form["operation"]

        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            if num1 == 0 or num2 == 0:
                return render_template("error_divide.html")
            result = num1 / num2
        return render_template("calculator.html", result=result)
    return render_template("calculator.html")

def allowed_file(filename):
    return "." in filename and \
            filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/image", methods=["GET", "POST"])
def image():
    images = []
    is_post = False
    if request.method == "POST":
        if "img" not in request.files:
            flash("No file")
            return render_template("error_image.html")
        file = request.files["img"]
        if file.filename == "":
            flash("No selected file")
            return render_template("error_image.html")
        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD"], file_name))
            images.append(os.path.join(app.config["UPLOAD"], file_name))
            is_post = True
            return render_template("image.html", images=images, is_post=is_post)
        else:
            flash("File type not allowed")
            return render_template("error_image.html")
    for file_name in os.listdir(app.config["UPLOAD"]):
        if allowed_file(file_name):
            images.append(os.path.join(app.config["UPLOAD"], file_name))
    return render_template("image.html", images=images, is_post=is_post)

if __name__ == "__main__":
    app.run()
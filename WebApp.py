import os
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
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
    return render_template("file_upload.html")

@app.route("/handle-get", methods=["GET"])
def handle_get():
    if request.method == "GET":
        username = request.args["username"]
        password = request.args["password"]
        if username in users and users[username] == password:
            return render_template("homepage.html")
        else:
            return render_template("error.html")
    else:
        return render_template("index.html")

@app.route("/handle-post", methods=["POST"])
def handle_post():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            return render_template("homepage.html")
        else:
            return render_template("error.html")
    else:
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
            result = num1 / num2
        else:
            result = "Invalid"

        return render_template("result.html", result=result)

def allowed_file(filename):
    return "." in filename and \
            filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/handle-file-upload", methods=["GET", "POST"])
def handle_file_upload():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file")
            return render_template("error.html")
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return render_template("error.html")
        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file_name))
            return render_template("file_success.html")
        else:
            flash("File type not allowed")
            return render_template("error.html")

if __name__ == "__main__":
    app.run()
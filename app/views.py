
from flask import render_template, request, redirect, url_for
from . import app


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/resume")
def resume():
    return render_template(
        "resume.html",
        title="Моє резюме",
        active_page="resume"
    )


@app.route("/contacts")
def contacts():
    return render_template(
        "contacts.html",
        title="Контакти",
        active_page="contacts"
    )


@app.route("/hi/<string:name>")
def greetings_page(name):
    name = name.upper()
    age = request.args.get("age", default=None, type=int)

    return f"{name} {age}"


@app.route("/admin")
def admin_page():
    return redirect(
        url_for("admin_info")
    )


@app.route("/admin/info")
def admin_info():
    return "ADMINISTRATOR 45"

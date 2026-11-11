
import logging
from pathlib import Path

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from . import app
from .forms import ContactForm


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


@app.route("/contact", methods=["GET", "POST"])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            # Налаштування запису в лог-файл
            logger = logging.getLogger("contact_form")

            if not logger.handlers:
                log_path = Path(current_app.root_path).parent / "contact.log"

                handler = logging.FileHandler(
                    log_path,
                    encoding="utf-8"
                )
                handler.setFormatter(logging.Formatter(
                    "%(asctime)s - %(levelname)s - %(message)s"
                ))

                logger.addHandler(handler)
                logger.setLevel(logging.INFO)

            # Запис даних форми
            logger.info(
                "Нове повідомлення: Ім'я: %s | Email: %s | "
                "Телефон: %s | Тема: %s | Повідомлення: %s",
                form.name.data,
                form.email.data,
                form.phone.data,
                form.subject.data,
                form.message.data
            )

            flash(
                "Ваше повідомлення успішно надіслано!",
                "success"
            )

        except OSError:
            current_app.logger.exception(
                "Помилка запису контактного повідомлення"
            )

            flash(
                "Не вдалося зберегти повідомлення. Спробуйте пізніше.",
                "danger"
            )

        # Post/Redirect/Get
        return redirect(url_for("contacts"))

    elif request.method == "POST":
        flash(
            "Форма містить помилки. Перевірте введені дані.",
            "danger"
        )

    return render_template(
        "contacts.html",
        form=form,
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
    return redirect(url_for("admin_info"))


@app.route("/admin/info")
def admin_info():
    return "ADMINISTRATOR 45"

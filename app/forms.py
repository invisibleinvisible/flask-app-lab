
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp
)


class ContactForm(FlaskForm):
    name = StringField(
        "Ваше ім'я",
        validators=[
            DataRequired(message="Введіть своє ім'я."),
            Length(
                min=4,
                max=10,
                message="Ім'я повинно містити від 4 до 10 символів."
            )
        ]
    )

    email = StringField(
        "Електронна пошта",
        validators=[
            DataRequired(message="Введіть електронну пошту."),
            Email(message="Введіть коректну електронну пошту.")
        ]
    )

    phone = StringField(
        "Номер телефону",
        validators=[
            DataRequired(message="Введіть номер телефону."),
            Regexp(
                r"^\+380\d{9}$",
                message="Формат телефону: +380XXXXXXXXX."
            )
        ]
    )

    subject = SelectField(
        "Тема звернення",
        choices=[
            ("question", "Запитання"),
            ("suggestion", "Пропозиція"),
            ("complaint", "Скарга"),
            ("other", "Інше")
        ],
        validators=[
            DataRequired(message="Оберіть тему звернення.")
        ]
    )

    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Введіть текст повідомлення."),
            Length(
                max=500,
                message="Повідомлення не повинно перевищувати 500 символів."
            )
        ]
    )


from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    SelectField,
    IntegerField,
    FileField
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    InputRequired,
    ValidationError
)
from flask_wtf.file import FileAllowed, FileSize



class ProductForm(FlaskForm):

    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Введіть назву товару."),
            Length(min=3, message="Назва повинна містити мінімум 3 символи.")
        ]
    )

    content = TextAreaField(
        "Опис товару",
        validators=[
            DataRequired(message="Введіть опис товару."),
            Length(max=2000, message="Опис не повинен перевищувати 2000 символів.")
        ]
    )

    price = DecimalField(
        "Ціна",
        places=None,
        validators=[
            InputRequired(message="Вкажіть ціну."),
            NumberRange(min=0.01, message="Ціна повинна бути більшою за нуль.")
        ]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("electronics", "Електроніка"),
            ("computers", "Комп'ютери"),
            ("phones", "Телефони"),
            ("accessories", "Аксесуари")
        ],
        validators=[
            DataRequired(message="Оберіть категорію.")
        ]
    )

    quantity = IntegerField(
        "Кількість",
        validators=[
            InputRequired(message="Вкажіть кількість."),
            NumberRange(min=0, message="Кількість не може бути від'ємною.")
        ]
    )

    image = FileField(
        "Зображення товару",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Дозволені лише JPG, JPEG та PNG."
            ),
            FileSize(max_size=2 * 1024 * 1024)
        ]
    )

    def validate_price(self, field):
        if field.data is not None:
            if field.data.as_tuple().exponent < -2:
                raise ValidationError(
                    "Ціна повинна мати не більше двох знаків після коми."
                )

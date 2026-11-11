from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_pyfile("../config.py")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

csrf = CSRFProtect(app)

from . import views
from .users import user_bp
from .products import products_bp


app.register_blueprint(user_bp)
app.register_blueprint(products_bp)
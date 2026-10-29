
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app,
    make_response,
)
from . import user_bp


# Демонстраційні облікові дані без бази даних
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "secret"


@user_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", default=None, type=int)

    return render_template(
        "users/hi.html",
        name=name,
        age=age
    )


@user_bp.route("/admin")
def admin():
    return redirect(
        url_for(
            "users.greetings",
            name="administrator",
            age=45
        )
    )


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("users.profile"))

        flash("Неправильний логін або пароль.", "danger")
        return redirect(url_for("users.login"))

    return render_template("users/login.html")


@user_bp.route("/profile", methods=["GET", "POST"])
def profile():
    username = session.get("username")

    if not username:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_cookie":
            key = request.form.get("cookie_key", "").strip()
            value = request.form.get("cookie_value", "")
            max_age_input = request.form.get("cookie_max_age", "").strip()

            if not key or key.lower() == current_app.config["SESSION_COOKIE_NAME"].lower():
                flash("Вкажіть коректний ключ cookie.", "danger")
                return redirect(url_for("users.profile"))

            if any(ord(char) < 33 or ord(char) > 126 or char in '()<>@,;:\\"/[]?={}' for char in key):
                flash("Ключ cookie містить недопустимі символи.", "danger")
                return redirect(url_for("users.profile"))

            max_age = None

            if max_age_input:
                try:
                    max_age = int(max_age_input)
                    if max_age <= 0:
                        raise ValueError
                except ValueError:
                    flash("Термін дії має бути додатним числом секунд.", "danger")
                    return redirect(url_for("users.profile"))

            response = make_response(redirect(url_for("users.profile")))
            response.set_cookie(
                key,
                value,
                max_age=max_age,
                httponly=True,
                samesite="Lax"
            )
            flash(f"Cookie «{key}» буде додано.", "success")
            return response

        elif action == "delete_cookie":
            key = request.form.get("delete_key", "").strip()

            if not key:
                flash("Вкажіть ключ cookie для видалення.", "warning")
                return redirect(url_for("users.profile"))

            if key == current_app.config["SESSION_COOKIE_NAME"]:
                flash("Не можна видаляти cookie сесії з профілю.", "danger")
                return redirect(url_for("users.profile"))

            if key not in request.cookies:
                flash(f"Cookie «{key}» не знайдено.", "warning")
                return redirect(url_for("users.profile"))

            response = make_response(redirect(url_for("users.profile")))
            response.delete_cookie(key, samesite="Lax")
            flash(f"Cookie «{key}» видалено.", "success")
            return response

        elif action == "delete_all_cookies":
            response = make_response(redirect(url_for("users.profile")))
            session_cookie = current_app.config["SESSION_COOKIE_NAME"]

            for key in request.cookies:
                if key != session_cookie:
                    response.delete_cookie(key, samesite="Lax")

            flash("Усі користувацькі cookies видалено.", "success")
            return response

        flash("Невідома операція.", "warning")
        return redirect(url_for("users.profile"))

    return render_template(
        "users/profile.html",
        username=username,
        cookies={
            key: value
            for key, value in request.cookies.items()
            if key != current_app.config["SESSION_COOKIE_NAME"]
        },
        theme=request.cookies.get("theme", "light")
    )


@user_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))


@user_bp.route("/set-theme/<theme_name>")
def set_theme(theme_name):
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    if theme_name not in ("light", "dark"):
        flash("Невідома кольорова схема.", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(
        "theme",
        theme_name,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="Lax"
    )

    flash("Кольорову схему змінено.", "success")
    return response

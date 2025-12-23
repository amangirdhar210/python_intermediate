from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user, error = AuthService.login(username, password)

        if error:
            flash(error, "error")
        else:
            flash("Logged in successfully!", "success")
            return redirect(url_for("main.dashboard"))

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        name = request.form.get("name")
        password = request.form.get("password")

        user, error = AuthService.register(email, username, name, password)

        if error:
            flash(error, "error")
        else:
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/logout")
def logout():
    AuthService.logout()
    flash("Logged out successfully!", "success")
    return redirect(url_for("auth.login"))

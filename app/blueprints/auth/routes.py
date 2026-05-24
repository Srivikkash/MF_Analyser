from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        if User.find_by_email(request.form["email"]):
            flash("Email already exists", "danger")
            return redirect(url_for("auth.signup"))
        User.create(request.form["email"], request.form["name"], request.form["password"])
        flash("Account created", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.find_by_email(request.form["email"])
        if user and user.check_password(request.form["password"]):
            login_user(user)
            return redirect(url_for("main.dashboard"))
        flash("Invalid credentials", "danger")
    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.dashboard"))

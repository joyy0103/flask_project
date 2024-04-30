from flask import Blueprint, render_template, redirect, url_for
from apps.app import db
from apps.crud.models import User, Gamelist
from apps.crud.forms import UserForm, GameForm
from apps.auth.forms import LoginForm

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@crud.route("/")
def index():
    return redirect(url_for("auth.login"))

@crud.route("/sql")
def sql():
    db.session.query(User).all()
    return "콘솔 로그를 확인해 주세요"

@crud.route("/users/new", methods=["GET", "POST"])
def create_user():
    form = UserForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )      
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))
    return render_template("crud/create.html", form=form)

@crud.route("/games/new/<user_email>", methods=["GET","POST"])
def create_game(user_email):
    form = GameForm()

    if form.validate_on_submit():
        gamelist = Gamelist(
            useremail=user_email,
            gamename=form.gamename.data,
        )

        db.session.add(gamelist)
        db.session.commit()

        return redirect(url_for("crud.game_index"))
    return render_template("crud/game_create.html", form=form)

@crud.route("/users")
def users():
    users = User.query.all()
    return render_template("crud/index.html", users=users)

@crud.route("/games")
def game_index():
    games = Gamelist.query.order_by("gamename").all()
    return render_template("crud/game_index.html", games=games)

@crud.route("/users/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    form = UserForm()

    # User 모델을 이용하여 사용자를 취득한다
    user = User.query.filter_by(id=user_id).first()

    # form으로부터 제출된 경우는 사용자를 갱신하여 사용자의 일람 화면으로 리다이렉트한다
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))

    # GET의 경우는 HTML을 반환한다
    return render_template("crud/edit.html", user=user, form=form)

@crud.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField(
        "메일 주소",
        validators=[
            DataRequired("메일 주소는 필수입니다."),
            Email("메일 주소의 형식으로 입력하세요."),
        ],
    )
    password = PasswordField("비밀번호", validators=[DataRequired("비밀번호는 필수입니다.")])
    submit = SubmitField("로그인")

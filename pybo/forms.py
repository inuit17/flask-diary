from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class DiaryWriteForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('꼭 써주세요!')])
    image = TextAreaField('이미지URL', validators=[DataRequired('꼭 써주세요!')])
    content = TextAreaField('내용', validators=[DataRequired('꼭 써주세요!')])
    hash = SelectField(u'--감정단어 고르기--',
                       choices=[('😄행복한', '😄행복한'),
                                ('😍흥분된', '😍흥분된'),
                                ('😲놀란', '😲놀란'),
                                ('😳간절한', '😳간절한'),
                                ('😨두려운', '😨두려운'),
                                ('😰불안한', '😰불안한'),
                                ('😅난감한', '😅난감한'),
                                ('🤔고민스러운', '🤔고민스러운'),
                                ('😞실망스러운', '😞실망스러운'),
                                ('😐덤덤한', '😐덤덤한'),
                                ('😒지루한', '😒지루한'),
                                ('😬불쾌한', '😬불쾌한'),
                                ('😔걱정스러운', '😔걱정스러운'),
                                ('😴피곤한', '😴피곤한'),
                                ('😢슬픈', '😢슬픈'),
                                ('😣참고 있는', '😣참고 있는'),
                                ('😤화난', '😤화난')])


class FeedbackForm(FlaskForm):
    content = TextAreaField('[알아가는 중이에요] 혹시 이런 느낌을 받으시나요?', validators=[DataRequired()])
    check = SelectField(u'--이런 느낌을 받으시나요?--', choices=[('네,그렇습니다.', '네,그렇습니다.'), ('아니오,그렇지 않습니다.', '아니오,그렇지 않습니다.')])


class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=2, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])


class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=2, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

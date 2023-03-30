from datetime import datetime
from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from .. import db
from ..forms import FeedbackForm
from ..models import Diary, Feedback

from .auth_views import login_required

bp = Blueprint('feedback', __name__, url_prefix='/feedback')


@bp.route('/create/<int:diary_id>', methods=('GET', 'POST'))
@login_required
def create(diary_id):
    form = FeedbackForm()
    diary = Diary.query.get_or_404(diary_id)
    if request.method == 'POST' and form.validate_on_submit():
        content = request.form['content']
        check = request.form['check']
        feedback = Feedback(content=content, check=check, user=g.user)  # check를 어떻게 표현하지
        diary.feedback_set.append(feedback)
        db.session.commit()
        return redirect(url_for('diary.detail', diary_id=diary_id))
    return render_template('diary/diary_detail.html', diary=diary, form=form)


@bp.route('/delete/<int:feedback_id>')
@login_required
def delete(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    diary_id = feedback.question.id
    if g.user != feedback.user:
        flash('지울 권한이 없어요!')
    else:
        db.session.delete(feedback)
        db.session.commit()
    return redirect(url_for('diary.detail', diary_id=diary_id))

# @bp.route('/create/', methods=('GET', 'POST'))
# def create():
#     form=DiaryWriteForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         diary = Diary(subject=form.subject.data, image=form.image.data, content=form.content.data, hash=form.hash.data, create_date=datetime.now())
#         db.session.add(diary)
#         db.session.commit()
#         return redirect(url_for('main.index'))
#     return render_template('diary/diary_form.html', form=form)
### 참고하기 위해서 가져온 코드
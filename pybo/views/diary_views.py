from datetime import datetime

from pybo.forms import DiaryWriteForm

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from pybo import db

from pybo.models import Diary, Feedback
from pybo.forms import DiaryWriteForm, FeedbackForm

from pybo.views.auth_views import login_required

bp = Blueprint('diary', __name__, url_prefix='/diary')


@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    diary_list = Diary.query.order_by(Diary.create_date.desc())
    diary_list = diary_list.paginate(page=page, per_page=20)
    return render_template('diary/diary_list.html', diary_list=diary_list)


@bp.route('/detail/<int:diary_id>/')
def detail(diary_id):
    form = FeedbackForm()
    diary = Diary.query.get_or_404(diary_id)
    return render_template('diary/diary_detail.html', diary=diary, form=form)


@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = DiaryWriteForm()
    if request.method == 'POST' and form.validate_on_submit():
        diary = Diary(subject=form.subject.data, image=form.image.data, content=form.content.data, hash=form.hash.data,
                      create_date=datetime.now(), user=g.user)
        db.session.add(diary)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('diary/diary_form.html', form=form)


@bp.route('/modify/<int:diary_id>', methods=('GET', 'POST'))
@login_required
def modify(diary_id):
    diary = Diary.query.get_or_404(diary_id)
    if g.user != diary.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('diary.detail', diary_id=diary_id))
    if request.method == 'POST':  # POST 요청
        form = DiaryWriteForm()
        if form.validate_on_submit():
            form.populate_obj(diary)
            diary.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('diary.detail', diary_id=diary_id))
    else:  # GET 요청
        form = DiaryWriteForm(obj=diary)
    return render_template('diary/diary_form.html', form=form)


@bp.route('/delete/<int:diary_id>')
@login_required
def delete(diary_id):
    diary = Diary.query.get_or_404(diary_id)
    if g.user != diary.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('diary.detail', diary_id=diary_id))
    db.session.delete(diary)
    db.session.commit()
    return redirect(url_for('diary._list'))


@bp.route('/modify/<int:feedback_id>', methods=('GET', 'POST'))
@login_required
def modify(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if g.user != feedback.user:
        flash('수정권한이 없어요!')
        return redirect(url_for('diary.detail', diary_id=feedback.diary.id))
    if request.method == "POST":
        form = FeedbackForm()
        if form.validate_on_submit():
            form.populate_obj(feedback)
            feedback.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('diary.detail', diary_id=feedback.diary.id))
    else:
        form = FeedbackForm(obj=feedback)
    return render_template('feedback/feedback_form.html', form=form)



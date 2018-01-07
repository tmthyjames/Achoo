from flask import render_template, Blueprint, redirect, url_for, flash, g
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from app.forms.forms import LoginForm
from app.models.models import User

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/sign-up', methods=['GET'])
def signup():
    return render_template('sign-up.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.capture'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        g.user = user
        return redirect(url_for('main.capture'))
    return render_template('login.html', title='Sign In', form=form)

@main.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/capture', methods=['GET'])
@login_required
def capture():
    return render_template('capture.html')

@main.route('/prediction', methods=['GET'])
@login_required
def prediction():
    return render_template('prediction.html')

@main.route('/my-dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('my-dashboard.html')

@main.errorhandler(401)
def page_not_found(e):
    form = LoginForm()
    return render_template('login.html', form=form, title='Sign In')

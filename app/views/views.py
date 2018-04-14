from flask import abort, Blueprint, flash, g, render_template, redirect, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from urllib.parse import urlparse, urljoin
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
            return redirect(url_for('main.login'))

        login_user(user)
        g.user = user

        nexturl = request.args.get('next')
        if not is_safe_url(nexturl):
            return abort(400)

        return redirect(nexturl or url_for('main.capture'), code=301)
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
def dashboard():
    return render_template('my-dashboard.html')


# auth

login_manager = LoginManager()

@login_manager.unauthorized_handler
def needs_login():
    return redirect(url_for('main.login', next=url_for(request.endpoint)))


# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

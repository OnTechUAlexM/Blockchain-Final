from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user, login_user
from .forms import LoginForm, SignupForm
from .models import db, User, Wallet
from . import login_manager, logger


auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@login_manager.user_loader
def load_user(user_id):
    """ Checks if the user is already logged in """
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """ Redirect to log in page if unauthorized """
    flash('You must be logged in to view that page')
    return redirect(url_for('auth_bp.login'), code=302)


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login page

    GET - serves log in page
    POST - validates user credentials
    """

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(password=form.password.data):
            login_user(user)
            if user.is_vendor:
                next_page = url_for('main_bp.dashboard', type="v")
            else:
                next_page = url_for('main_bp.dashboard', type="u")
            return redirect(next_page, code=302)

        flash('Invalid username or password')
        return redirect(url_for('auth_bp.login'), code=302)

    return render_template(
        'login.html',
        form=form
    )


@auth_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    Signup page

    GET - serves signup page.
    POST - validates form and user creation.
    """
    form = SignupForm()
    if form.validate_on_submit():

        # Checking if the email have been used
        existing_user = User.query.filter_by(email=form.email.data).first()

        if not existing_user:
            # Create user account
            user = User(
                email=form.email.data
            )

            # Sets password using sha256
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)

            # Initializes user wallet
            u = User.query.filter_by(user.email).first()
            w = Wallet(
                uid=u.id,
                amt=5000.0
            )
            db.session.add(w)
            db.session.commit()

            return redirect(url_for('main_bp.dashboard', type='u'), code=302)

        flash('Email already in use.')

    return render_template(
        'signup.html',
        title='Create an Account.',
        form=form,
    )

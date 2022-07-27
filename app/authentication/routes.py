from flask import Blueprint, render_template, request, redirect, url_for
from app.forms import UserSignInForm, UserSignUpForm
from app.models import User, db, check_password_hash, Favorite, Artist
from flask_login import login_user, logout_user, login_required, current_user
from config import Config

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signin', methods=["GET", "POST"])
def signin():
    form = UserSignInForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                return redirect(url_for('auth.profile'))
            else:
                print("Email or Password Incorrect")
                return redirect(url_for('auth.signin'))
        else:
            print("form not valid")
    except:
        raise 
    return render_template('signin.html', form=form)

@auth.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserSignUpForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            artist = form.artist.data

            user = User(email, password, first_name, last_name, artist)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('auth.signin'))
    except:
        raise

    return render_template('signup.html', form=form)

@auth.route('/profile', methods=["GET"])
@login_required
def profile():
    subquery = db.session.query(Favorite.artist_id).filter(Favorite.user_id == current_user.id)
    print(subquery)
    artists = db.session.query(Artist).filter(Artist.id.in_(subquery))
    print(artists)

    print(current_user.email)
    email = current_user.email
    admin_email = Config.ADMIN_EMAIL
    return render_template('profile.html', artists = artists, email = email, admin_email = admin_email)

@auth.route('/logout')
@login_required
def logout():
    print(f"now logging out {current_user.first_name}")
    logout_user()
    print("you are now logged out")
    return redirect(url_for('site.home'))


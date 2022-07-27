from crypt import methods
from unicodedata import category
from urllib.parse import urlencode
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import subquery
from app.forms import ArtistRegistryForm, FeedbackForm, FavoriteButton, DeletePending, AcceptPending
from cloudinary import uploader
from app.models import Favorite, Pending, db, Artist
from config import Config
from app.api.routes import delete_pending







site = Blueprint('site', __name__, template_folder='site_templates')


@site.route('/', methods=["GET","POST"])
def home():
    home = True
    form = FeedbackForm()
    return render_template('index.html', form=form, home = home)


@site.route('/gallery/<category>', methods=["GET", "POST"])
def gallery(category):
    page_value = 0
    if category == "traditional":
        page_value = 1
    elif category == "japanese":
        page_value = 2
    elif category == "realism":
        page_value = 3
    elif category == "surrealism":
        page_value = 4
    elif category == "abstract":
        page_value = 5
    elif category == "minimalism":
        page_value = 6
    elif category == "blackwork":
        page_value = 7
    elif category == "geometric":
        page_value = 8
    else:
        page_value = 0
    
    artist = Artist.query.all()


    return render_template('gallery.html', page_value = page_value, artist = artist)




@site.route('/artist/<id>', methods=["GET", "POST"])
def artist(id):

    artist = Artist.query.get(id)
    category = artist.category.lower()
    form = FavoriteButton()
    
    form.submit_button.label.text = "Confirm"

    if request.method == "POST" and form.validate_on_submit():
        if current_user.is_authenticated:
            user_fav = db.session.query(Favorite).filter(Favorite.user_id == current_user.id, Favorite.artist_id == artist.id).first()

            print(user_fav)
            if user_fav:
                print("You already have this artist in your watchlist!")
                return redirect(url_for('site.gallery', category = category))
            else:
                if form.add_artist.data:
                    favorite = Favorite(artist_id = id, user_id = current_user.id)
                    print(favorite)
                    db.session.add(favorite)
                    db.session.commit()
                    return redirect(url_for('site.gallery', category = category))
                else:
                    return redirect(url_for('site.gallery', category = category))
        else:
            return redirect(url_for('auth.signin'))
    else:
        print("nono")

    return render_template('artist.html', form = form, artist = artist)


@site.route('/register', methods=["GET","POST"])
@login_required
def register():
    form = ArtistRegistryForm()
    
    try:
        if request.method == "POST" and form.validate_on_submit():
            image = form.image.data
            nickname = form.nickname.data
            email = form.email.data
            category = form.category.data
            country = form.country.data
            social = form.social.data

            cloudinary_upload_result = uploader.upload(image)
            # Sending the image file to cloudinary's endpoint, returning an object which holds our image url

            # print(cloudinary_upload_result)
            print(cloudinary_upload_result['url'])
            pending_artist = Pending(cloudinary_upload_result['url'], email, nickname, category, country, social, current_user.id)

            db.session.add(pending_artist)
            db.session.commit()

            return redirect(url_for('site.home'))
        else:
            print("didn't work")
    except:
        raise

    return render_template('register.html', form=form)





# Admin routes allowing for accepting and deleting Pending Artists
@site.route('/admin', methods=['GET','POST'])
@login_required
def admin():
    email = current_user.email
    admin_email = Config.ADMIN_EMAIL

    if email == admin_email:
        pending = Pending.query.all()
        acceptform = AcceptPending(request.form)
        deleteform = DeletePending(request.form)

        return render_template('admin.html', pending_artists = pending, acceptform = acceptform, deleteform = deleteform)
    else:
        return redirect(url_for('site.home'))

@site.route('/admin/accept', methods=['GET','POST'])
@login_required
def admin_accept():
    email = current_user.email
    admin_email = Config.ADMIN_EMAIL

    if email == admin_email:
        pending = Pending.query.all()
        acceptform = AcceptPending(request.form)
        deleteform = DeletePending(request.form)

        if acceptform.validate_on_submit():
            image = acceptform.image.data
            email = acceptform.email.data
            nickname = acceptform.nickname.data
            category = acceptform.category.data
            country = acceptform.country.data
            social = acceptform.social.data
            user_id = acceptform.user_id.data

            artist = Artist(image, email, nickname, category, country, social, user_id)

            db.session.add(artist)
            db.session.commit()

            delete_pending(user_id)

            return redirect(url_for('site.admin'))
        else:
            print("something not right on accept")

        return render_template('admin.html', pending_artists = pending, acceptform = acceptform, deleteform = deleteform)
    else:
        return redirect(url_for('site.home'))

@site.route('/admin/delete', methods=['GET', 'POST'])
@login_required
def admin_delete():
    email = current_user.email
    admin_email = Config.ADMIN_EMAIL

    if email == admin_email:
        pending = Pending.query.all()
        acceptform = AcceptPending(request.form)
        deleteform = DeletePending(request.form)


        if deleteform.validate_on_submit():
            pending_id = deleteform.pending_id.data

            delete_pending(pending_id)
            return redirect(url_for('site.admin'))
        else:
            print("something not right on delete")

        return render_template('admin.html', pending_artists = pending, acceptform = acceptform, deleteform = deleteform)
    else:
        return redirect(url_for('site.home'))


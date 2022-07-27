from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from sqlalchemy import Sequence

# being imported in auth routes
from werkzeug.security import generate_password_hash, check_password_hash
# converts password in form into a hash string of random characters, checks hash to its original form

import secrets
# generates a token for a user
from flask_login import UserMixin, LoginManager

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
# creating the ORM that maps python data from a model into a SQL table
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Models in desscending order by relationship link


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=False)
    artist_question = db.Column(db.String(3), nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    date_create = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    pending_artist = db.relationship('Pending', backref='owner', lazy=True)
    favorites = db.relationship('Favorite', backref='liked_artist', lazy=True)

    # All artists may come from a user id in which the user is an artist
    # All users will be able to add an artist to their favorites

    def __init__(self, email, password, first_name='', last_name='', artist_question='', id='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password)
        self.artist_question = artist_question
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())
        # generates a unique set of characters and integers for a difficult id rather than a guessable serial

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
        # taken from werkzeug.security library

    def __repr__(self):
        return f"User {self.email} has been added to the database"


# Created pending artist model to hold users' requests to be displayed as an artist
class Pending(db.Model):
    id = db.Column(db.String, primary_key=True)
    image = db.Column(db.String, nullable=False)
    email = db.Column(db.String(150), nullable=False)
    nickname = db.Column(db.String(150), nullable=True, default='')
    category = db.Column(db.String(150), nullable=False, default='')
    country = db.Column(db.String(150), nullable= True, default ='')
    social = db.Column(db.String(150), nullable=False, default='')
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=True)

    # TODO: change user_id nullable = True to False when ready for production

    def __init__(self, image, email, nickname='', category='', country = '', social='', user_id='', id=''):
        self.id = self.set_id()
        self.image = image
        self.email = email
        self.nickname = nickname
        self.category = category
        self.country = country
        self.social = social
        self.user_id = user_id

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"You are now pending as Pending Artist"


# Create Artist Model
class Artist(db.Model):
    id = db.Column(db.String, primary_key=True)
    image = db.Column(db.String, nullable=False)
    email = db.Column(db.String(150), nullable=False)
    nickname = db.Column(db.String(150), nullable=True, default='')
    category = db.Column(db.String(150), nullable=False, default='')
    country = db.Column(db.String(150), nullable= True, default ='')
    social = db.Column(db.String(150), nullable=False, default='')
    user_id = db.Column(db.String(150), nullable=True, default='')
    date_create = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    favorites = db.relationship('Favorite', backref='liked_by', lazy=True)

    def __init__(self, image, email, nickname='', category='', country='', social='', user_id='', id=''):
        self.id = self.set_id()
        self.image = image
        self.email = email
        self.nickname = nickname
        self.category = category
        self.country = country
        self.social = social
        self.user_id = user_id

    def set_id(self):
        return str(uuid.uuid4())

    def __repr__(self):
        return f"User {self.email} has been added as an Artist database"


# Creating a Favorites Model with User ID relationship in which you can query filter favorites based on artist in which logged user id is the match

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    artist_id = db.Column(db.String, db.ForeignKey('artist.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, artist_id='', user_id=''):
        self.artist_id = artist_id
        self.user_id = user_id

    def __repr__(self):
        return "Artist added to your Watchlist!"


# Marshmallow Schemas

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "first_name", "last_name", "email",
                  "artist_question", "date_create")


user_schema = UserSchema()  # allows grabbing one model by id
users_schema = UserSchema(many=True)


class PendingSchema(ma.Schema):
    class Meta:
        fields = ("id", "image", "email", "nickname",
                  "category", "country", "social", "user_id")


pending_schema = PendingSchema()
pendings_schema = PendingSchema(many=True)


class ArtistSchema(ma.Schema):
    class Meta:
        fields = ("id", "image", "email", "nickname",
                  "category", "country", "social", "user_id", "date_create")


artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)


class FavoriteSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "artist_id")


favorite_schema = FavoriteSchema()
favorites_schema = FavoriteSchema(many=True)

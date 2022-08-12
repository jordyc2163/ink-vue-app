from crypt import methods
import json
from flask import Blueprint, request, jsonify
from app.models import User, Artist, Pending, Favorite, user_schema, users_schema, pending_schema, pendings_schema, artist_schema, artists_schema, favorite_schema, favorites_schema, db

api = Blueprint('api', __name__, url_prefix='/api')

# API Data Methods


# GET METHODS #

# Users
@api.route('/user', methods=['GET'])
def get_users():
    users = User.query.order_by(User.first_name).all()
    response = users_schema.dump(users)

    return jsonify(response)


@api.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    response = user_schema.dump(user)

    return jsonify(response)


# Pending Artists
@api.route('/pending', methods=['GET'])
def get_pending():
    pendings = Pending.query.order_by(Pending.id).all()
    response = pendings_schema.dump(pendings)

    return jsonify(response)


@api.route('/pending/<id>', methods=['GET'])
def get_pendings(id):
    pending = Pending.query.get(id)
    response = pending_schema.dump(pending)

    return jsonify(response)

# Artists


@api.route('/artist', methods=['GET'])
def get_artists():
    artists = Artist.query.order_by(Artist.date_create).all()
    response = artists_schema.dump(artists)

    return jsonify(response)


@api.route('/artist/<id>', methods=['GET'])
def get_artist(id):
    artist = Artist.query.get(id)
    response = artist_schema.dump(artist)

    return jsonify(response)

# Favorites


@api.route('/favorite', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.order_by(Favorite.id).all()
    response = favorites_schema.dump(favorites)

    return jsonify(response)


@api.route('/favorite/<id>', methods=['GET'])
def get_favorite(id):
    favorite = favorite.query.get(id)
    response = favorite_schema.dump(favorite)

    return jsonify(response)


# POST METHODS #

#  Artist

@api.route('/artist', methods=['POST'])
def create_artist():
    image = request.json['image']
    email = request.json['email']
    nickname = request.json['nickname']
    category = request.json['category']
    country = request.json['country']
    social = request.json['social']
    user_id = request.json['user_id']

    artist = Artist(image, email, nickname, category, country, social, user_id)

    if user_id:
        delete_pending(user_id)
    # if the artist was added through pending table, delete them from pending after instantiating as an artist

    db.session.add(artist)
    db.session.commit()

    response = artist_schema.dump(artist)

    return jsonify(response)

# Favorite


@api.route('/favorite', methods=['POST'])
def create_favorite():
    user_id = request.json['user_id']
    artist_id = request.json['artist_id']

    favorite = Favorite(artist_id, user_id)

    db.session.add(favorite)
    db.session.commit()

    response = artist_schema.dump(favorite)
    return jsonify(response)


# DELETE METHODS #

# User

@api.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    response = user_schema.dump(user)
    return jsonify(response)

# Artist


@api.route('/artist/<id>', methods=['DELETE'])
def delete_artist(id):
    artist = Artist.query.get(id)
    db.session.delete(artist)
    db.session.commit()

    response = artist_schema.dump(artist)
    return jsonify(response)

# Pending Artist - done once accepted or rejected


@api.route('/pending/<id>', methods=['DELETE'])
def delete_pending(id):
    pending = Pending.query.filter_by(user_id=id).first()
    db.session.delete(pending)
    db.session.commit()

    response = artist_schema.dump(pending)
    return jsonify(response)


# Delete Favorites
@api.route('/favorite/<user_id>/<artist_id>', methods=['DELETE'])
def delete_favorite(user_id, artist_id):
    artist = db.session.query(Favorite).filter(Favorite.user_id == user_id, Favorite.artist_id == artist_id).first()

    db.session.delete(artist)
    db.session.commit()
    
    response = favorite_schema.dump(artist)

    return jsonify(response)

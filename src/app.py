"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def handle_all_people():

    all_people = db.session.execute(db.select(People)).scalars().all()

    serialized_people = [person.serialize() for person in all_people]

    return jsonify(serialized_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    
    person = db.session.execute(db.select(People).filter_by(id=people_id)).scalar_one_or_none()

    if person is None:
        raise APIException("Person not found", status_code=404)

    serialized_person = person.serialize()

    return jsonify(serialized_person), 200

@app.route('/planet', methods=['GET'])
def handle_all_planet():

    all_planet = db.session.execute(db.select(Planet)).scalars().all()

    serialized_planet = [planet.serialize() for planet in all_planet]

    return jsonify(serialized_planet), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    
    planet = db.session.execute(db.select(Planet).filter_by(id=planet_id)).scalar_one_or_none()

    if planet is None:
        raise APIException("planet not found", status_code=404)

    serialized_planet = planet.serialize()

    return jsonify(serialized_planet), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = db.session.execute(db.select(User)).scalars().all()
    serialized_users = [user.serialize() for user in all_users]
    return jsonify(serialized_users), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
    if user is None:
        raise APIException("User not found", status_code=404)

    user_favorites = db.session.execute(db.select(favorite).filter_by(user_id=user_id)).scalars().all()
    serialized_favorites = [fav.serialize() for fav in user_favorites]

    return jsonify(serialized_favorites), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    body = request.get_json()
    if body is None:
        raise APIException("You must send a JSON body with user_id", status_code=400)
    if "user_id" not in body:
        raise APIException("The 'user_id' field is required", status_code=400)

    user_id = body["user_id"]

    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
    if user is None:
        raise APIException("User not found", status_code=404)
    planet = db.session.execute(db.select(Planet).filter_by(id=planet_id)).scalar_one_or_none()
    if planet is None:
        raise APIException("Planet not found", status_code=404)

    existing_favorite = db.session.execute(
        db.select(favorite).filter_by(user_id=user_id, planet_id=planet_id)
    ).scalar_one_or_none()

    if existing_favorite:
        raise APIException("Planet already in favorites for this user", status_code=409) 

    new_favorite = favorite(
        user_id=user_id,
        planet_id=planet_id,
        people_id=None,
        specie_id=None,
        starship_id=None,
        vehicle_id=None
    )
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Planet added to favorites successfully!", "favorite_id": new_favorite.id}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    body = request.get_json()
    if body is None:
        raise APIException("You must send a JSON body with user_id", status_code=400)
    if "user_id" not in body:
        raise APIException("The 'user_id' field is required", status_code=400)

    user_id = body["user_id"]

    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
    if user is None:
        raise APIException("User not found", status_code=404)
    person = db.session.execute(db.select(People).filter_by(id=people_id)).scalar_one_or_none()
    if person is None:
        raise APIException("Person not found", status_code=404)

    existing_favorite = db.session.execute(
        db.select(favorite).filter_by(user_id=user_id, people_id=people_id)
    ).scalar_one_or_none()

    if existing_favorite:
        raise APIException("Person already in favorites for this user", status_code=409)

    new_favorite = favorite(
        user_id=user_id,
        people_id=people_id,
        planet_id=None,
        specie_id=None,
        starship_id=None,
        vehicle_id=None
    )
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Person added to favorites successfully!", "favorite_id": new_favorite.id}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    body = request.get_json()
    if body is None:
        raise APIException("You must send a JSON body with user_id", status_code=400)
    if "user_id" not in body:
        raise APIException("The 'user_id' field is required", status_code=400)

    user_id = body["user_id"]

    favorite_to_delete = db.session.execute(
        db.select(favorite).filter_by(user_id=user_id, planet_id=planet_id)
    ).scalar_one_or_none()

    if favorite_to_delete is None:
        raise APIException("Favorite planet not found for this user", status_code=404)

    db.session.delete(favorite_to_delete)
    db.session.commit()

    return jsonify({"msg": "Favorite planet deleted successfully!"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    body = request.get_json()
    if body is None:
        raise APIException("You must send a JSON body with user_id", status_code=400)
    if "user_id" not in body:
        raise APIException("The 'user_id' field is required", status_code=400)

    user_id = body["user_id"]

    
    favorite_to_delete = db.session.execute(
        db.select(favorite).filter_by(user_id=user_id, people_id=people_id)
    ).scalar_one_or_none()

    if favorite_to_delete is None:
        raise APIException("Favorite person not found for this user", status_code=404)


    db.session.delete(favorite_to_delete)
    db.session.commit()

    return jsonify({"msg": "Favorite person deleted successfully!"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

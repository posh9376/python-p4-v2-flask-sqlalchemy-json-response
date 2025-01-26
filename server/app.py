# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)


@app.route('/demo_json')
def demo_json():
    pet = Pet.query.first()
    pet_dict = {'id': pet.id,
            'name': pet.name,
            'species': pet.species
            }
    return make_response(pet_dict, 200)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter_by(id=id).first()
    if pet:
        body = {'id': pet.id,
                'name': pet.name,
                'species': pet.species
                }
        return make_response(body, 200)
    else:
        body = {'message': f'Pet {id} not found'}
        return make_response(body, 404)

@app.route('/species/<string:species>')
def pet_by_species(species):
    pets =Pet.query.filter_by(species=species).all()
    pet_arr = []
    if pets:
        for pet in pets:
            pet_dict = {'id': pet.id,
                        'name': pet.name,}
            pet_arr.append(pet_dict)
        body = {'count': len(pet_arr),
                'pets': pet_arr}
        return make_response(body, 200)
    else:
        body = {'message': f'No pets found for species {species}'}
        return make_response(body, 404)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

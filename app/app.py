#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from flask import Flask, request, jsonify, make_response
from sqlalchemy.exc import IntegrityError, DataError

from models import db, Hero, Powers, HeroPowers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

# for the routes add the following

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    output = []
    for hero in heroes:
        output.append({'id' : hero.id, 
                       'name' : hero.name, 
                       'super_name' : hero.super_name})
    return jsonify(output)

@app.route('/heroes/<id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return make_response(jsonify({'error': 'Hero not found'}), 404)
    powers = [{'id': power.id, 
               'name': power.name, 
               'description': power.description} for power in hero.powers]
    return jsonify({'id' : hero.id, 
                    'name' : hero.name, 
                    'super_name' : hero.super_name, 
                    'powers': powers})

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Powers.query.all()
    output = []
    for power in powers:
        output.append({'id' : power.id, 
                       'name' : power.name, 
                       'description' : power.description})
    return jsonify(output)

@app.route('/powers/<id>', methods=['GET'])
def get_power(id):
    power = Powers.query.get(id)
    if not power:
        return make_response(jsonify({'error': 'Power not found'}), 404)
    return jsonify({'id' : power.id, 
                    'name' : power.name, 
                    'description' : power.description})

@app.route('/powers/<id>', methods=['PATCH'])
def update_power(id):
    power = Powers.query.get(id)
    if not power:
        return make_response(jsonify({'error': 'Power not found'}), 404)
    try:
        power.description = request.json['description']
        db.session.commit()
    except (IntegrityError, DataError):
        return make_response(jsonify({'errors': ['validation errors']}), 400)
    return jsonify({'id' : power.id, 
                    'name' : power.name, 
                    'description' : power.description})

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    power_id = request.json['power_id']
    hero_id = request.json['hero_id']
    strength = request.json['strength']
    try:
        new_hero_power = HeroPowers(hero_id=hero_id, power_id=power_id, strength=strength)
        db.session.add(new_hero_power)
        db.session.commit()
        hero = Hero.query.get(hero_id)
        powers = [{'id': power.id, 
                   'name': power.name, 
                   'description': power.description} for power in hero.powers]
        return jsonify({'id' : hero.id, 
                        'name' : hero.name, 
                        'super_name' : hero.super_name, 
                        'powers': powers}), 201
    except (IntegrityError, DataError):
        return make_response(jsonify({'errors': ['validation errors']}), 400)
    



if __name__ == '__main__':
    app.run(port=5555, debug=True)
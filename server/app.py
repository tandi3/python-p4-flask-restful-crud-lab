#!/usr/bin/env python3
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return {'message': 'Plant Store API', 'endpoints': ['/plants']}

# GET all plants
@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants]), 200

# GET plant by id
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return make_response({"error": "Plant not found"}, 404)
    return jsonify(plant.to_dict()), 200

# PATCH plant by id
@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return make_response({"error": "Plant not found"}, 404)

    data = request.get_json()
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']

    db.session.commit()
    return jsonify(plant.to_dict()), 200

# DELETE plant by id
@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return make_response({"error": "Plant not found"}, 404)

    db.session.delete(plant)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(port=5555)

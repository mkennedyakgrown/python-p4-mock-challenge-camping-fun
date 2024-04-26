#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


class Campers(Resource):

    def get(self):
        return [camper.to_dict() for camper in Camper.query.all()], 200
    
    def post(self):
        req_json = request.get_json()
        camper = Camper()
        try:
            camper.name = req_json.get('name')
            camper.age = req_json.get('age')
            db.session.add(camper)
            db.session.commit()
            return camper.to_dict(), 201
        except:
            return {'errors': ['validation errors']}, 400
    
class CamperById(Resource):

    def get(self, id):
        camper = Camper.query.filter_by(id=id).first()
        if camper is not None:
            camper_dict = camper.to_dict()
            camper_dict['signups'] = [
                Signup.query.filter_by(id=signup.id).first().to_dict()
                for signup in camper.signups]
            return camper_dict, 200
        else:
            return {'error': 'Camper not found'}, 404
    
    def patch(self, id):
        camper = Camper.query.filter_by(id=id).first()
        if camper is not None:
            json = request.get_json()
            try:
                camper.name = json.get('name')
                camper.age = json.get('age')
                db.session.add(camper)
                db.session.commit()
                return camper.to_dict(), 202
            except:
                return {'errors': ['validation errors']}, 400
        else:
            return {'error': 'Camper not found'}, 404
        
class Activities(Resource):

    def get(self):
        return [act.to_dict() for act in Activity.query.all()], 200
    
class ActivityById(Resource):
    
    def delete(self, id):
        act = Activity.query.filter_by(id=id).first()
        if act is not None:
            db.session.delete(act)
            db.session.commit()
            return {}, 204
        else:
            return {'error': 'Activity not found'}, 404
        
class Signups(Resource):
    
    def post(self):
        json = request.get_json()
        signup = Signup()
        try:
            signup.camper_id = json.get('camper_id')
            signup.activity_id = json.get('activity_id')
            signup.time = json.get('time')
            db.session.add(signup)
            db.session.commit()
            return signup.to_dict(), 201
        except:
            return {'errors': ['validation errors']}, 400
        

api.add_resource(Campers, '/campers', endpoint='campers')
api.add_resource(CamperById, '/campers/<int:id>')
api.add_resource(Activities, '/activities', endpoint='activities')
api.add_resource(ActivityById, '/activities/<int:id>')
api.add_resource(Signups, '/signups', endpoint='signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

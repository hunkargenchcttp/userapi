# Projeyi 2 aşamalı ele aldım.
# Hedef:    Client kısmında datayı üretip server a request kütüphanesi ile post etmeyi hedefledim.
# Eksikler: Data belirtilen model ile üretildi. 
#           Ancak data tipleri konusunda post ederken sorun yaşadım: birthday, latitude, longitude
          

from flask import Flask, request
from faker import Faker
from flask import jsonify,json
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema,fields
import requests,json

fake = Faker('tr_TR')
app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql:///userapi'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False



db=SQLAlchemy(app)
db.init_app(app=app)

class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    first_name=db.Column(db.String(255),nullable=False)
    last_name=db.Column(db.String(255),nullable=False)
    address=db.Column(db.String(255),nullable=False)
    birthday=db.Column(db.Date)
    latitude=db.Column(db.Float(18,16),nullable=False)
    longitude=db.Column(db.Float(18,16),nullable=False)

    def __repr__(self):
        return self.first_name

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class UserSchema(Schema):
    id=fields.Integer()
    first_name=fields.String()
    last_name=fields.String()
    address=fields.String()
    birthday=fields.DateTime()
    latitude=fields.Float()
    longitude=fields.Float()

@app.route('/users',methods=['GET'])
def get_all_users():
    users=User.get_all()

    serializer=UserSchema(many=True)

    data=serializer.dump(users)

    return jsonify(
        data
    )

@app.route('/users',methods=['POST'])
def create_a_user():
    data=request.get_json()

    new_user=User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        address=data.get('address'),
        birthday=data.get('birthday'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
    )

    new_user.save()

    serializer=UserSchema()

    data=serializer.dump(new_user)

    return jsonify(
        data
    ),201

@app.route('/user/<int:id>',methods=['GET'])
def get_user(id):
    user=User.get_by_id(id)

    serializer=UserSchema()

    data=serializer.dump(user)

    return jsonify(
        data
    ),200

@app.route('/user/<int:id>',methods=['PUT'])
def update_user(id):
    user_to_update=User.get_by_id(id)

    data=request.get_json()

    user_to_update.first_name=data.get('first_name')
    user_to_update.last_name=data.get('last_name')
    user_to_update.address=data.get('address')
    user_to_update.birthday=data.get('birthday')
    user_to_update.latitude=data.get('latitude')
    user_to_update.longitude=data.get('longitude')

    db.session.commit()

    serializer=UserSchema()

    user_data=serializer.dump(user_to_update)

    return jsonify(user_data),200

@app.route('/user/<int:id>',methods=['DELETE'])
def delete_user(id):
    user_to_delete=User.get_by_id(id)

    user_to_delete.delete()

    return jsonify({"message":"Deleted"}),204


@app.errorhandler(404)
def not_found(error):
    return jsonify({"message":"Resource not found"}),404

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message":"There is a problem"}),500


@app.route("/", methods=["POST", "GET"])
def index():

    first_name = fake.first_name()
    last_name = fake.last_name()
    address = fake.address()
    birthday = fake.date_of_birth()
    latitude = fake.latitude()
    longitude = fake.longitude()
    response = {
        "first_name": first_name,
        "last_name": last_name,
        "address": address,
        "birthday": birthday,
        "latitude": latitude,
        "longitude": longitude,
    }

    # endpoint = "/"
    # r = requests.post(endpoint,data=json.dumps(response,default=str))

    return jsonify(
        response
    )

if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0')
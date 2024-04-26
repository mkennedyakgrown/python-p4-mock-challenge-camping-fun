from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    campers = association_proxy('signups', 'camper', creator=lambda camper_obj: Signup(camper=camper_obj))

    signups = db.relationship('Signup', back_populates='activity', cascade='all, delete-orphan')
    
    serialize_only = ('id', 'name', 'difficulty')
    serialize_rules = ('-campers.activities', '-signup.activity')
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    activities = association_proxy('signups', 'activity', creator=lambda activity_obj: Signup(activity=activity_obj))

    signups = db.relationship('Signup', back_populates='camper', cascade='all, delete-orphan')
    
    serialize_only = ('id', 'name', 'age')
    serialize_rules = ('-activities.campers', '-activities.signups', '-signup.activities' '-signup.camper')
    
    @validates('name')
    def validate_name(self, key, name_text):
        if name_text == "" or name_text is None:
            raise ValueError('Name cannot be empty')
        return name_text
    
    @validates('age')
    def validate_age(self, key, age_int):
        if type(age_int) != int:
            raise TypeError('Age must be an integer')
        if age_int < 8 or age_int > 18:
            raise ValueError('Age must be between 8 and 18')
        return age_int
    
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    camper = db.relationship('Camper', uselist=False, back_populates='signups')

    activity = db.relationship('Activity', uselist=False, back_populates='signups')
    
    serialize_rules = ('-activity.signup', '-camper.signup', '-activity.camper', '-camper.activity')
    
    @validates('time')
    def validate_time(self, key, time_int):
        if time_int < 0 or time_int > 23:
            raise ValueError('Time must be between 0 and 23')
        return time_int
    
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.

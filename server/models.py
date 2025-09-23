from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# Models go here!

class Food(db.Model, SerializerMixin):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    carbs = db.Column(db.Integer, nullable=False, default=0)
    gi = db.Column(db.Integer, nullable=False, default=0)
    serving_grams = db.Column(db.Integer, nullable=False, default=0)

    serialize_rules = ('-metadata',)

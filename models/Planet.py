from models.Db_Init import db
from sqlalchemy import Column, Integer, String, Float
from marshmallow import Schema


class Planet(db.Model):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)


class PlanetSchema(Schema):
    class Meta:
        fields = ('id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')


planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

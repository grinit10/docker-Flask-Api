from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, JWTManager
from flask_migrate import Migrate
import os

from config import config_by_name
from models.Db_Init import db
from models.Planet import Planet, planet_schema, planets_schema
from models.User import User

app: Flask = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config.from_object(config_by_name[os.getenv('BOILERPLATE_ENV') or 'dev'])
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created')


@app.cli.command('db_update')
def db_update():
    db.update(User)
    print('Database updated')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped')


@app.cli.command('db_seed')
def db_drop():
    mercury = Planet(planet_name='Mercury', planet_type='Class D', home_star='Sol', mass=3.258e23, radius=1516,
                     distance=35.98e6)
    venus = Planet(planet_name='Venus', planet_type='Class K', home_star='Sol', mass=4.867e24, radius=3760,
                   distance=67.24e6)
    earth = Planet(planet_name='Earth', planet_type='Class M', home_star='Sol', mass=5.972e24, radius=3959,
                   distance=92.96e6)
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)
    test_user = User(first_name='Arnab', last_name='Chakraborty', email='grinit10@gmail.com', password='Password123')
    db.session.add(test_user)
    db.session.commit()
    print('Database seeded')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def hello_simple_world():
    return {
               'message': 'Hello World!'
           }, 200


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return {
                   'message': 'Sorry ' + name + ', You are not 18 yet.'
               }, 401
    else:
        return {
                   'name': 'Welcome, ' + name + '.'
               }, 200


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(age: int, name: str):
    if age < 18:
        return {
                   'message': 'Sorry ' + name + ', You are not 18 yet.'
               }, 401
    else:
        return {
                   'name': 'Welcome, ' + name + '.'
               }, 200


@app.route('/planets', methods=['GET'])
@jwt_required
def list_planets():
    planets = Planet.query.all()
    result = planets_schema.dump(planets)
    return jsonify(result)


@app.route('/planets/<int:id>', methods=['GET'])
@jwt_required
def get_planet(id: int):
    planet = Planet.query.filter_by(id=id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result)
    else:
        return {
                   'message': 'No planet with the id found'
               }, 404


@app.route('/planets', methods=['POST'])
@jwt_required
def add_planet():
    if Planet.query.filter_by(planet_name=request.form['planet_name']).first():
        return {
                   'message': 'The planet already exists'
               }, 404
    else:
        planet_name = request.form['planet_name']
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = float(request.form['mass'])
        radius = float(request.form['radius'])
        distance = float(request.form['distance'])
        planet = Planet(planet_name=planet_name, radius=radius, distance=distance, home_star=home_star,
                        planet_type=planet_type, mass=mass)
        db.session.add(planet)
        db.session.commit()
        return jsonify({
            'message': 'Planet is created successfully'
        }), 201


@app.route('/planets', methods=['PUT'])
@jwt_required
def update_planet():
    planet = Planet.query.filter_by(id=request.form['id']).first()
    if planet:
        planet.planet_name = request.form['planet_name']
        planet.planet_type = request.form['planet_type']
        planet.home_star = request.form['home_star']
        planet.mass = float(request.form['mass'])
        planet.radius = float(request.form['radius'])
        planet.distance = float(request.form['distance'])
        db.session.commit()
        return jsonify({
            'message': 'Planet is updated successfully'
        }), 202
    else:
        return {
                   'message': 'The planet does not exist'
               }, 404


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {
                   'message': 'Email already exists'
               }, 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return {
                   'message': 'User created successfully'
               }, 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        access_token = create_access_token(identity=email)
        return {
                   'message': 'Logged in successfully',
                   'access_token': access_token
               }, 200
    else:
        return {
                   'message': 'Bad email or password',
               }, 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

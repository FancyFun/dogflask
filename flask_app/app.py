from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Dog.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
    
    DB.init_app(app)

    @app.route('/')
    def home():

        return 'success the flask app is running!'

    @app.route('/render')
    def render():
        return render_template('home.html')

    @app.route('/render_with_insert/<insert>')
    def render_insert(insert):
        return render_template('insert.html',insertion=insert)

    @app.route('/puppy')
    def puppy():
        json = requests.get('https://dog.ceo/api/breeds/image/random').json()
        image = json['message']

        return render_template('dog.html', picture=image, blob=json)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return 'DB reset'

    @app.route('/save_dog')
    def save_dog():
        json = requests.get('https://dog.ceo/api/breeds/image/random').json()
        image = json['message']
        return render_template('save_dog.html', picture=image)

    @app.route('/saved_dog', methods=['POST'])
    def saved_dog():
        image = request.values['doglink']
        name = request.values['dogname']
        dog = Dog(dog=image,name=name)

        DB.session.add(dog)
        DB.session.commit()
        return render_template('saved_dog.html', picture=image, name=name)

    @app.route('/dog_list')
    def dog_list():
        dogs = Dog.query.all()
        names = [dog.name for dog in dogs]
        return render_template('dog_list.html', names=names)

    @app.route('/view_dog', methods=['POST'])
    def view_dog():
        name = request.values['dogname']
        dog = Dog.query.filter_by(name=name).all()[0]

        return render_template('saved_dog.html', picture=dog.dog, name=dog.name)

    return app

    ##########################################################

DB = SQLAlchemy()

class Dog(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    dog = DB.Column(DB.Text)
    name = DB.Column(DB.Text)

    def __repr__(self):
        return f'{self.name} is dog number {self.id}'
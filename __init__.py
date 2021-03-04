import os
import psycopg2
import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# get environment variable
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_PORT = os.getenv('DB_PORT')
app.debug = True
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(150), unique=False)
    last_name = db.Column(db.String(150), unique=False)
    email = db.Column(db.String(150), unique=False)
    gender = db.Column(db.String(7), unique=False)
    date_of_birth = db.Column(db.String(20), unique=False)
    country_of_birth = db.Column(db.String(150), unique=False)

    def __init__(self, id, first_name, last_name, email, gender,
                 date_of_birth, country_of_birth):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.country_of_birth = country_of_birth


class dbConnection():
    def __init__(self):
        self.conn = psycopg2.connect(user=DB_USER,
                                     password=DB_PASSWORD,
                                     host=DB_HOST,
                                     port=DB_PORT,
                                     database=DB_DATABASE
                                     )
        self.cur = self.conn.cursor()
        print("DB connection created")

    def query(self, psql_query, data):
        try:
            self.cur.execute(psql_query, data)
            result = self.cur.fetchall()
            return result
        except Exception as exception:
            print(exception)


@app.route('/ping')
def ping():
    return {'pong': datetime.datetime.today()}, 200


@app.route('/get_user_data/<int:id>', methods=['GET'])
def get_user_data(id):
    psql = '''SELECT * FROM person WHERE id = %s'''
    conn = dbConnection()
    result = conn.query(psql, (id,))
    return jsonify({'data': result})


@app.route('/create_user', methods=['POST'])
def create_task():
    create_person = request.get_json()
    person = Person(id=create_person['id'], first_name=create_person['first_name'],
                    last_name=create_person['last_name'], email=create_person['email'],
                    gender=create_person['gender'], date_of_birth=create_person['date_of_birth'],
                    country_of_birth=create_person['country_of_birth'])
    db.session.add(person)
    db.session.commit()
    return jsonify(create_person)


app.run(debug=True, host='0.0.0.0', port=8081)


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@127.0.0.1:5432/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


"""This Class used To Create Table person with two columns id , name """
class Person(db.Model):
  __tablename__ = 'persons'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)

  def __repr__(self):
     return f'Person ID: {self.id}, name: {self.name}'

""" This line will check class persons if exist on database or not if its not exist it will add it """
db.create_all()


@app.route('/')

def index():
    person=Person.query.first()
    return 'Hello ' + person.name
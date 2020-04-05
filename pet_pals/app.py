# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
# from config import db_username, db_password
from flask_pymongo import PyMongo

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
  app.debug = True
  app.config['MONGO_URI'] = 'mongodb://localhost:27017/flask-mongo-db'
else:
  app.debug = False
  username = os.environ.get('DATABASE_USERNAME', '')
  password = os.environ.get('DATABASE_PASSWORD', '')
  app.config['MONGO_URI'] = f'mongodb+srv://{username}:{password}@cluster0-laoqs.mongodb.net/test?retryWrites=true&w=majority'
  app.config['MONGO_DBNAME'] = 'flask-mongo-db'

mongo = PyMongo(app)

@app.route("/")
def home():
    return render_template("index.html")

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

  australia_data = {
    "state": "New South Wales",
    "fatalities": 25,
    "homes_lost": 2439,
    "area_ha": 54000000,
    "area_acres": 13300000,
  }

  mongo.db.australia_2019_2020_fire_season.update({}, australia_data, upsert=True)

  # Redirect back to home page
  return redirect("/")


if __name__ == "__main__":
    app.run()

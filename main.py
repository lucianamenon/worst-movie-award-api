import traceback
from http import HTTPStatus
from flask import Flask, jsonify

import app.config as config
import app.utils as utils
import app.database as database

from app.models import Movie, Producer, MovieProducer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route('/api/v1/texo/check', methods=['GET'])
def health_check():
    """Health check route"""
    return jsonify({}), 204

@app.route('/api/v1/texo/producers-award-interval', methods=['GET'])
def get_producer_interval():
    data = utils.get_min_max_interval()
    return jsonify(data), 200

@app.route('/api/v1/texo/movies', methods=['GET'])
def get_movies():
    data = Movie.get_all()
    return jsonify(menssage="List of movies", data=data), 200

@app.route('/api/v1/texo/producers', methods=['GET'])
def get_producers():
    data = Producer.get_all()
    return jsonify(menssage="List of producers", data=data), 200

@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
@app.errorhandler(Exception)
def unexpected_error(e):
    """Handle exceptions by returning swagger-compliant json."""
    code = '500'
    message = 'The server encountered an internal error and was unable to complete your request.'
    print(print(traceback.format_exc()))
    return jsonify(code=code, menssage=message), 500

if __name__ == '__main__':
    with app.app_context():
        try:
            database.db.init_app(app)
            database.db.create_all()
            utils.populate_tables(config.MOVIES_DATA_PATH)
        except Exception as e:
            print('The server encountered an internal error and was unable to start. Check your configuration file!')
            print(e)
        else:
            app.run(host='0.0.0.0', debug=False)

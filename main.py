from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus

import app.config as config

app = Flask(__name__)

#DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

@app.route('/api/v1/texo/check', methods=['GET'])
def health_check():
    """Health check route"""
    return jsonify({}), 204

@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
@app.errorhandler(Exception)
def unexpected_error(e):
    """Handle exceptions by returning swagger-compliant json."""
    code = '500'
    message = 'The server encountered an internal error and was unable to complete your request.'
    print(e)
    return jsonify(code=code, menssage=message), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

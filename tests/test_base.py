from flask_testing import TestCase

from app import database
from main import app

class BaseTestCase(TestCase):
    def create_app(self):
        with app.app_context():
            app.config['TESTING'] = True
            database.db.init_app(app)
            database.db.create_all()
        return app

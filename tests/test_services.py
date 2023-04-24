import unittest
from tests.test_base import BaseTestCase
from app.services import CSVService, MinMaxService

class TestService(BaseTestCase):

    def test_integrations(self):

        #populate_tables: correct cvs populate_tables
        self.assertEqual(CSVService.populate_tables("tests/movielist.csv"), (206, 472))
        #get_min_max_interval: correct challenge response
        self.assertEqual(MinMaxService.get_min_max_interval(), {'min': [{'producer': 'Joel Silver', 'interval': 1, 'previousWin': 1990, 'followingWin': 1991}], 'max': [{'producer': 'Matthew Vaughn', 'interval': 13, 'previousWin': 2002, 'followingWin': 2015}]})

        #empty table, empty min max objects
        self.assertEqual(CSVService.populate_tables("tests/movielist-2.csv"), (0, 0))
        self.assertEqual(MinMaxService.get_min_max_interval(), {'min': [], 'max': []})

        #no winners with multiple awards
        self.assertEqual(CSVService.populate_tables("tests/movielist-3.csv"), (206, 472))
        self.assertEqual(MinMaxService.get_min_max_interval(), {'min': [], 'max': []})

        #same min max
        self.assertEqual(CSVService.populate_tables("tests/movielist-4.csv"), (206, 472))
        self.assertEqual(MinMaxService.get_min_max_interval(), {"max": [{"followingWin": 1991, "interval": 1, "previousWin": 1990, "producer": "Joel Silver"}], "min": [{"followingWin": 1991, "interval": 1, "previousWin": 1990, "producer": "Joel Silver"}]})

        #multiple min max
        self.assertEqual(CSVService.populate_tables("tests/movielist-5.csv"), (208, 474))
        self.assertEqual(MinMaxService.get_min_max_interval(), {'min': [{'producer': 'Joel Silver', 'interval': 1, 'previousWin': 1990, 'followingWin': 1991}], 'max': [{'producer': 'Matthew Vaughn', 'interval': 13, 'previousWin': 2002, 'followingWin': 2015}, {'producer': 'Pluto Nash', 'interval': 13, 'previousWin': 2002, 'followingWin': 2015}]})

        #service health check endpoint
        response = self.client.get('/api/v1/texo/check')
        self.assertEqual(response.status_code, 204)
        #service other endpoints
        response = self.client.get('/api/v1/texo/producers')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1/texo/movies')
        self.assertEqual(response.status_code, 200)
        #complete service test endpoint get_min_max_interval after populate_tables: correct cvs populate_tables
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CSVService.populate_tables("tests/movielist.csv"), (206, 472))
        response = self.client.get('/api/v1/texo/producers-award-interval')
        self.assertEqual(response.json, {'min': [{'producer': 'Joel Silver', 'interval': 1, 'previousWin': 1990, 'followingWin': 1991}], 'max': [{'producer': 'Matthew Vaughn', 'interval': 13, 'previousWin': 2002, 'followingWin': 2015}]})


if __name__ == '__name__':
    unittest.main()
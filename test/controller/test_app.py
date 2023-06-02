import unittest
from flask import Response
from graph_app.controller.app import app
import os


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Change the CWD to the root folder
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        os.chdir(root_dir)

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        # Create mock files and data
        self.player_name_line = 'T. Cleverley'
        self.compare_name_line = 'A. Masina'
        self.start_date = '2018-12-16'
        self.end_date = '2020-12-16'
        self.player_name_radar = 'J. Timber'
        self.compare_name_radar = 'L. Geertruida'
        self.league = 'Eredivisie'
        self.stat = 'Defensive duels / won'

    def check_assertions(self, response):
        # Assert the response
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'image/png')
        self.assertIsInstance(response.data, bytes)

    def test_line_endpoint(self):
        response = self.app.post('/graph/line',
                                 data={
                                     'player': self.player_name_line,
                                     'compare': self.compare_name_line,
                                     'stat': self.stat,
                                     'start-date': self.start_date,
                                     'end-date': self.end_date
                                 },
                                 content_type='multipart/form-data')
        self.check_assertions(response)

    def test_radar_endpoint(self):
        response = self.app.post('/graph/radar',
                                 data={
                                     'player': self.player_name_radar,
                                     'compare': self.compare_name_radar,
                                     'league': self.league
                                 },
                                 content_type='multipart/form-data')
        self.check_assertions(response)

    def random_endpoint(self, graph):
        response = self.app.post('/graph',
                                 data=graph,
                                 content_type='multipart/form-data')
        self.check_assertions(response)

    def test_random_endpoint(self):
        self.random_endpoint({})

    def test_random_endpoint_line(self):
        self.random_endpoint({"graph-type": "line"})

    def test_random_endpoint_radar(self):
        self.random_endpoint({"graph-type": "radar"})


if __name__ == "__main__":
    unittest.main()

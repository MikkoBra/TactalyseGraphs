import unittest
from unittest.mock import patch, MagicMock
from graph_app.data.preprocessors.line_processor import LineProcessor


class TestLineProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = LineProcessor()

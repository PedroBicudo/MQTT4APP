"""Testes unitarios em mqtt4app."""
from mqtt4app import Mqtt4App
import unittest


class Mqtt4AppTests(unittest.TestCase):
    """Classes de testes unitarios."""

    def setUp(self):
        self.mqtt4app = Mqtt4App(
            topics=['a', 'b', 'c'], 
            back_db_name='teste'
            )

    def test_connection(self):
        pass

    def test_tuple_to_list(self):
        result = self.mqtt4app._convert_to_tuple_list(list('abc'))
        answer =[('a', 0), ('b', 0), ('c', 0)]
        self.assertEqual(
            result, answer,
            f"{result} deveria ser {answer}."
            )

    def test_get_class_path(self):
        result = self.mqtt4app._get_class_path()
        self.assertEqual(
            result, "/classes/teste/", 
            f"{result} deveria ser /classes/teste/"
        )

    def tearDown(self):
        self.mqtt4app.disconnect()
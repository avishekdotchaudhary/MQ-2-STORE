import unittest
from unittest.mock import patch
from mq_app.app import run_publisher
from mq_app.rabbitmq.services.publisher_service import is_json


class TestCddPublisher(unittest.TestCase):

    def test_is_json_valid(self):
        valid_json = '{"name": "test"}'
        self.assertTrue(is_json(valid_json))

    def test_is_json_invalid(self):
        invalid_json = '{name: test}'
        self.assertFalse(is_json(invalid_json))

    def test_is_json_non_json(self):
        non_json = "Hello World"
        self.assertFalse(is_json(non_json))

    def test_is_json_int(self):
        non_json = 423
        self.assertFalse(is_json(non_json))

    # Test run_publisher with mocked PublisherService
    @patch('mq_app.rabbitmq.services.publisher_service.PublisherService')
    def test_run_publisher(self, MockPublisherService):
        data = '{"name": "Alice", "age": 30, "city": "New York"}'

        run_publisher(data)

if __name__ == '__main__':
    unittest.main()

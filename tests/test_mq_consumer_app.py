import unittest
from unittest.mock import patch, MagicMock
from mq_app.app import run_consumer


class TestCddConsumer(unittest.TestCase):

    @patch('mq_app.rabbitmq.services.consumer_service.ConsumerService')
    def test_run_consumer(self, MockConsumerService):
        mock_consumer = MagicMock()
        MockConsumerService.return_value = mock_consumer

        run_consumer()

        mock_consumer.consume_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()

import logging, json, os

from mq_app.rabbitmq.services.consumer_service import ConsumerService
from mq_app.config.logging_config import setup_logging
from mq_app.rabbitmq.services.publisher_service import PublisherService


setup_logging()

# Entry point to publish json data.
def save_message(data_to_publish):
    # Create an instance of the PublisherService class and call its publish_json method to send the provided data to the queue.
    publisher_service = PublisherService()
    publisher_service.publish_json(data_to_publish)

# Entry point to consume json data and store it to MongoDB.
def consume_messages():
    # Create an instance of the ConsumerService class and invoke its consume_json method to process incoming messages.
    consumer_service = ConsumerService()
    consumer_service.consume_json()

# This function is used to check the input is json or not.
# def is_json(data):
#     # Check if data is a string
#     if isinstance(data, str) and isinstance(data, dict):
#         return True
#     try:
#         # Try to parse the string into JSON
#         return isinstance(json.loads(data), dict)
#     except (json.JSONDecodeError, TypeError):
#         logging.error(f'Invalid JSON: {data}')
#         return False

# def publisher_consumer(input_data):
#     if is_json(input_data):
#         run_publisher(input_data)
#         run_consumer()
#
# ind = '{"name": "Alice", "age": 30, "city": "New York"}'
# publisher_consumer(ind)
import pika, os, logging, json
from dotenv import load_dotenv, find_dotenv
from mq_app.constants import RabbitMQConstants
from mq_app.config.config import load_config

if not load_dotenv(find_dotenv()):
    load_dotenv(os.path.join(os.getcwd(), '.env'))
else:
    load_dotenv(find_dotenv())

class PublisherService:
    def __init__(self):
        self.url = None
        rabbitmq_uri = os.getenv("RABBIT_MQ_URL")
        queue_name = os.getenv("QUEUE_NAME")
        exchange_name = os.getenv("EXCHANGE_NAME")
        exchange_type = os.getenv("EXCHANGE_TYPE")
        self.config = load_config()
        self.rabbitmq_host = rabbitmq_uri
        self.connection = None
        self.channel = None
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.routing_key = queue_name

    # This method is used to create connection
    def create_connection(self):
        if not self.rabbitmq_host:
            raise ValueError(f"Rabbitmq host doesn't exist. {self.rabbitmq_host}")
        self.url = pika.URLParameters(self.rabbitmq_host)
        self.connection = pika.BlockingConnection(self.url)

    def create_channel(self):
        self.channel = self.connection.channel()

    # This method is used to close the connection
    def close_connection(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    # This method is used to close the channel
    def close_channel(self):
        if self.channel and self.channel.is_open:
            self.connection.close()

    # This method is used to publish the message to the rabbitmq
    def publish_mq(self, data):

        self.create_connection()
        self.create_channel()

        if not self.exchange_name:
            logging.warning(f"Exchange name is None. Using 'default_exchange'.")
            self.exchange_name = RabbitMQConstants.RABBITMQ_EXCHANGE_NAME

        if not self.queue_name:
            logging.warning(f"Queue name is None. Using 'default_queue'.")
            self.queue_name = RabbitMQConstants.RABBITMQ_QUEUE_NAME

        if not self.routing_key:
            logging.warning(f"Routing key is None. Using 'default_queue'.")
            self.routing_key = RabbitMQConstants.RABBITMQ_QUEUE_NAME

        if not self.exchange_type:
            logging.warning(f"Exchange type is None. Using 'direct'.")
            self.exchange_type = RabbitMQConstants.RABBITMQ_EXCHANGE_TYPE

        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)
        self.channel.queue_declare(queue=self.queue_name, durable=True)

        # Define message properties (persistent)
        properties = pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent
        )

        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=data,
            properties=properties
        )

        logging.info(f'[->] Sent JSON data to queue. {data}')
        self.close_channel()
        self.close_connection()

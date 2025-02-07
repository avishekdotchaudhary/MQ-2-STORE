import pika, os, logging
from mq_app.monog.services.mongo_service import MongoDBService
from dotenv import load_dotenv, find_dotenv
from mq_app.config.config import load_config
from mq_app.constants import RabbitMQConstants

if not load_dotenv(find_dotenv()):
    load_dotenv(os.path.join(os.getcwd(), '.env'))
else:
    load_dotenv(find_dotenv())

class ConsumerService:
    def __init__(self):
        rabbitmq_uri = os.getenv("RABBIT_MQ_URL")
        collection_name = os.getenv("MONGO_COLLECTION_NAME")
        queue_name = os.getenv("QUEUE_NAME")
        exchange_name = os.getenv("EXCHANGE_NAME")
        exchange_type = os.getenv("EXCHANGE_TYPE")
        self.config = load_config()
        self.rabbitmq_host = rabbitmq_uri
        self.mongo_collection_name = collection_name
        self.mongo_service = MongoDBService()
        self.connection = None
        self.channel = None
        self.url = None
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

    # This method is used to close connection
    def close_connection(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    # This method is used to close channel
    def close_channel(self):
        if self.channel and self.channel.is_open:
            self.channel.close()

    # THis method is used to consume message from rabbitmq
    def consume_mq(self):
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
        self.channel.queue_bind(queue=self.queue_name, exchange=self.exchange_name, routing_key=self.routing_key)

        def callback(ch, method, properties, body):
            if not self.mongo_collection_name:
                logging.warning(f"Collection name is None. Using 'cost_data_dump'.")
                self.mongo_collection_name = RabbitMQConstants.MONGO_COLLECTION_NAME

            try:
                data = body.decode()
                self.mongo_service.insert_data(self.mongo_collection_name, data)
                ch.basic_ack(delivery_tag=method.delivery_tag) # Acknowledge the message
                logging.info(f'[~] Message consumed successfully.')
            except Exception as e:
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True) # Requeue the message
                logging.error(f'[~] Message failed to consume: {e}')

        logging.info(f'[~] Waiting for messages.....')
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback)
        self.channel.start_consuming()
        
        self.close_channel()
        self.close_connection()
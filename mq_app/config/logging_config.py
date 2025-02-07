import logging, os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from mq_app.config.config import load_config

log_dir = os.path.abspath(os.path.join(os.getcwd(), 'logs'))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

def setup_logging():
    config = load_config()
    log_file = os.path.join(log_dir, f"cdd_app_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    # Create the rotating file handler
    rotating_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7, encoding='utf-8')
    rotating_handler.setLevel(config['cdd']['logging']['rotating_level'])
    rotating_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Configure the logging system
    logging.basicConfig(
        level=config['cdd']['logging']['level'],
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            rotating_handler
        ]
    )

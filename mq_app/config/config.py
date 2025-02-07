import yaml, os

def load_config(config_file='config.yml'):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'mq_app'))
    config_path = os.path.join(root_dir, config_file)

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    return config
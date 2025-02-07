# MQ-2-STORE
This project provides a simple solution for integrating RabbitMQ with a database. Users can import the package to:

- Publish a messages to RabbitMQ.
- Consume those messages.
- Store the processed data into a database.

It’s ideal for use cases that require reliable message handling and persistence.

---
# ✅ Requirements

- 🛢️ MongoDB – Database
- 📩 RabbitMQ – Message Queue
- 🐍 Python 3.x
- 📦 pymongo – MongoDB client
- 📨 pika – RabbitMQ client
- 🔧 python-dotenv – For environment variables
---

# 🚀 Installation

- Clone Project and build wheel package:
    ```sh
    git clone https://github.com/avishekdotchaudhary/MQ-2-STORE.git
- Change Directory   
   ```sh  
   cd MQ-2-STORE
- Build wheel package
    ```sh
    python setup.py bdist_wheel
- Install wheel package via `pip`:
    ```sh
    pip install mq_app-1.0.0-py3-none-any.whl
---
# 📖 Usage

- To run consumer create python file `consumer.py`.
    ```python
    from mq_app import app
    
    app.consume_messages()
- To run publisher create another python file `publisher.py`.
    ````python
    from mq_app import app
    
    app.save_message({"message": "Hello, World!"})
---
# 🔧 Configuration

- You need to create a `.env` file in the root directory, add the configuration below, and update the `URLs` if you're using hosted `RabbitMQ` and `MongoDB`. Similarly, update the `MONGO_DB_NAME` and `MONGO_COLLECTION_NAME` as needed.
  ````.env
  RABBITMQ_URL=amqp://guest:guest@localhost:5672/
  MONGO_URI=mongodb://localhost:27017/
  MONGO_DB_NAME=mydatabase
  MONGO_COLLECTION_NAME=mq_store
---
# 🛠 Features

- ✅ Queue JSON messages using 📩 RabbitMQ.
- ✅ Store messages in 🛢️MongoDB.
- ✅ Simple and easy-to-use 📦 Package.
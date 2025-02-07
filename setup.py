from setuptools import setup, find_packages

# Open README.md with UTF-8 encoding to avoid UnicodeDecodeError
with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="mq_app",                # Your package name
    version="0.0.1",                  # Your package version
    author="Avishek Chaudhary",               # Your name
    author_email="avishekdotchaudhary@gmail.com",  # Your email
    description="This package queues a messages using RabbitMQ and efficiently stores them in MongoDB.",  # Description of your project
    long_description=long_description,  # Detailed description from README
    long_description_content_type="text/markdown",  # Optional: specify markdown
    url="https://github.com/avishekdotchaudhary/MQ-2-STORE",  # Your project's URL
    packages=find_packages(),         # Automatically discover all packages
    install_requires=[
        'pika', 'pymongo', 'pyyaml', 'python-dotenv' # Dependencies
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6', # Minimum Python version
    include_package_data=True, # Include additional files (like config.yml, .env)
    package_data={
            '': ['./*.yml', './*.md'],  # Include all .yml files from the root directory
        },
)
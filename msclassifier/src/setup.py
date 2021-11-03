from setuptools import setup

setup(
    name="Backend",
    version="1.0",
    description="Backend for Classifier Microservice",
    install_requires=[
        'SQLAlchemy',
        'scikit-learn',
        'psycopg2-binary',
        'psycopg2',
        'pandas',
        'flask',
        'flask-cors',
        'numpy==1.19.5'
    ]
)

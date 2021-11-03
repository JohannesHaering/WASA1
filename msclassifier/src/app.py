from flask import Flask
from flask_cors import CORS
import psycopg2

from api.API import API, apirouter
from api.BackendForFrontend import BackendForFrontend, bffrouter
import config as cfg

print("Checking database")
connection = None
try:
    datastring = "dbname='{}' user='{}' host='{}' password='{}' port='{}'".format(cfg.postgresql['databasename'], cfg.postgresql['databaseuser'],    cfg.postgresql['databaseip'], cfg.postgresql['password'], cfg.postgresql['port'])
    connection = psycopg2.connect(datastring)
except Exception as err:
    print(err)
    print("Database is not connected. Aborting...")
    exit()
print('Database is connected')
print('Check if tables exist')

try:
    cur = connection.cursor()
    cur.execute("select * from information_schema.tables")
    tables = cur.fetchall()
    modelExist = False
    modelUsageExist = False
    for table in tables:
        if table[2] == 'model':
            modelExist = True
        if table[2] == 'modelUsage':
            modelUsageExist = True
    if modelExist and modelUsageExist:
        print("Tables are existing")
    else:
        print("Missing tables")
        exit()
except Exception as err:
    print(err)

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(apirouter)
app.register_blueprint(bffrouter)

app.run(host=cfg.flask["host"])

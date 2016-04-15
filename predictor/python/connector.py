# -*- coding: utf-8 -*-
### The inclusions ###
import os
from sqlalchemy import create_engine
### /inclusions ###

# Getting the environ DB info
user = os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME')
passwd = os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD')
host = os.environ.get('OPENSHIFT_MYSQL_DB_HOST')
port = os.environ.get('OPENSHIFT_MYSQL_DB_PORT')
database = os.environ.get('OPENSHIFT_APP_NAME')

# Connecting to the database
engineString = "mysql://{0}:{1}@{2}:{3}/{4}".format(user, passwd, host, port, database) 
engine = create_engine(engineString)
connection = engine.connect()
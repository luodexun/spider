# -*- coding: utf-8 -*-

# 生产环境／测试环境
PRODUCTION = True
if PRODUCTION:
    LOG_LEVEL = 'INFO'

    MONGO_HOST = 'mongodb://admin:kete123@121.201.55.116'
    MONGO_PORT = 27017
    MONGO_DB = 'kete_data'

    REDIS_URL = 'redis://:kete123@121.201.55.116:6379/0'

    # MYSQL_HOST = '58.82.225.91'
    # MYSQL_PORT = 3306
    # MYSQL_USER = 'root'
    # MYSQL_PASSWORD = 'kete789'
    # MYSQL_DB_NAME = 'kete_data'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'localhost'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB_NAME = 'kete_data'
    MYSQL_CHARSET = 'utf8'
else:
    LOG_LEVEL = 'DEBUG'

    MONGO_HOST = 'mongodb://admin:kete123@121.201.55.116'
    MONGO_PORT = 27017
    MONGO_DB = 'kete_data'

    REDIS_URL = 'redis://127.0.0.1:6379/0'

    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'rose123'
    MYSQL_DB_NAME = 'kete_data'
    MYSQL_CHARSET = 'utf8'
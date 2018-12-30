# -*- coding: utf-8 -*-

# 生产环境／测试环境
PRODUCTION = False
if PRODUCTION:
    LOG_LEVEL = 'INFO'

    MYSQL_HOST = 'rm-wz9j5b719265n6z9deo.mysql.rds.aliyuncs.com'
    MYSQL_PORT = 3306
    MYSQL_USER = 'dwnchain'
    MYSQL_PASSWORD = 'Dwn1118#yyy'
    MYSQL_DB_NAME = 'test'
    MYSQL_CHARSET = 'utf8'
else:
    LOG_LEVEL = 'DEBUG'
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'ldx574425450'
    MYSQL_DB_NAME = 'shop'
    MYSQL_CHARSET = 'utf8'
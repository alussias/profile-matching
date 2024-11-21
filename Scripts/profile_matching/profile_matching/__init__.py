import pymysql
# Disable real cursor and use server-side cursor instead
pymysql.install_as_MySQLdb()
pymysql.version_info = (1, 4, 2, 'final', 0)
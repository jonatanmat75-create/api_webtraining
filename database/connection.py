import pymysql

def get_connection():

    return pymysql.connect(
        host="localhost",
        user="root",
        password="Sena2026*",
        database="web_training",
        cursorclass=pymysql.cursors.DictCursor
    )

import sys
sys.path.insert(0,"/home/grupo4daw24/DawRiders/myenv/lib/python3.10/site-packages/")

import pymysql

def obtener_conexion():
    return pymysql.connect(host='grupo4daw24.mysql.pythonanywhere-services.com',
                                user='grupo4daw24',
                                password='plis12345',
                                db='grupo4daw24$cicloriders')
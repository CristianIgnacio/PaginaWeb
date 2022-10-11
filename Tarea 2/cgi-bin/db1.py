#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mysql.connector

import cgitb


cgitb.enable()

class DB:
    def __init__(self, host, user, password, database):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db.cursor()

    def save_order(self, data):

            sql ='''
                INSERT INTO viaje (origen, destino, fecha_ida, fecha_regreso, kilos_disponible, espacio_disponible, email_viajero, celular_viajero) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                '''
            self.cursor.execute(sql, data)  # ejecuto la consulta
            self.db.commit()                # modifico la base de datos
            

    def get_data(self):
        
        sql = '''
            SELECT * FROM pizza
            '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_viaje(self, id_viaje):
        
        sql = f'''
            SELECT * FROM viaje WHERE id  = "{id_viaje}"
            '''

        self.cursor.execute(sql)
        return self.cursor.fetchall()
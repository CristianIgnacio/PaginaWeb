#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mysql.connector
import hashlib
import sys
import cgi
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

        try:
            sql ='''
                INSERT INTO encargo (descripcion, espacio, kilos, origen, destino, email_encargador, celular_encargador) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''
            self.cursor.execute(sql, data[1:8])  # ejecuto la consulta
            id_encargo = self.cursor.getlastrowid() # recupera el último id ingresado
            print("hola")
            fileobj = data[0]
            for archivo in fileobj:
                filename = archivo.filename

                sql = "SELECT COUNT(id) FROM foto" # Cuenta los archivos que hay en la base de datos
                self.cursor.execute(sql)
                total = self.cursor.fetchall()[0][0] + 1
                filename_hash = hashlib.sha256(filename.encode()).hexdigest()[0:30] # aplica función de hash
                filename_hash += f"_{total}" # concatena la función de hash con el número total de archivos, nombre único
                # OJO: lo anterior puede ser peligroso en el caso en que se tenga un servidor que ejecute peticiones en paralelo.
                #       Lo que se conoce como un datarace
                open(f"../media/{filename_hash}", "wb").write(archivo.file.read()) # guarda el archivo localmente
                sql_file = '''
                    INSERT INTO foto (ruta_archivo, nombre_archivo, encargo_id) 
                    VALUES (%s, %s, %s)
                    '''
                self.cursor.execute(sql_file, (filename_hash, filename, id_encargo))  # ejecuta la query que guarda el archivo en base de datos
            
            # guardar pedido
            self.db.commit()                # modifico la base de datos
            
        except:
            print("ERROR AL GUARDAR EN LA BASE DE DATOS")
            sys.exit()

    def get_data(self):
        
        sql = '''
            SELECT * FROM pizza
            '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_encargo(self, id_encargo):
        
        sql = f'''
            SELECT * FROM encargo WHERE id  = "{id_encargo}"
            '''

        self.cursor.execute(sql)
        return self.cursor.fetchall()
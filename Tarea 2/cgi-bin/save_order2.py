#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import os
import sys
import re
import cgitb
from db2 import DB

cgitb.enable()

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)

#Localizamos la base de datos
db = DB('localhost', 'cc500219_u', 'eporttitor', 'cc500219_db')
form = cgi.FieldStorage()

descripcion_encargo = form.getvalue('descripcion-encargo')

espacio = form.getvalue('espacio-solicitado')
kilos = form.getvalue('kilos-solicitado')

pais_origen = form.getvalue('pais-origen')
ciudad_origen = form.getvalue('ciudad-origen')

pais_destino = form.getvalue('pais-destino')
ciudad_destino = form.getvalue('ciudad-destino')

foto_encargo = form['foto-encargo']

email_encargo = form.getvalue('email')
celular_encargo = form.getvalue('celular')

# Validar los campos
errores = ''
errores2 = ''   

Tipos_espacios = ["10x10x10","20x20x20","30x30x30"]
Tipos_kilos = ["200 gr","500 gr","800 gr","1 kg","1.5 kg","2 kg"]

regex_email = r"/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/"
regex_email = r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$"

regex_celular = "^\\+?\d{9,15}$"
regex_celular = r"^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$/"
regex_celular = r"(\+56)?([0-9][-]*){9}$"
regex_celular = r"^(\(?\+[\d]{1,3}\)?)\s?([\d][\s\.-]?){8,9}$"

MAX_FILE_SIZE = 100000000
tipos_soportados = ['image/jpeg', 'image/jpg', 'image/png']

if pais_origen != "":
    comando_pais_origen = "SELECT id FROM pais WHERE nombre='"+ pais_origen +"'"
    db.cursor.execute(comando_pais_origen)
    id_pais_origen = db.cursor.fetchall()[0][0]

if ciudad_origen != "": 
    comando_ciudad_origen = "SELECT pais FROM ciudad WHERE nombre='"+ ciudad_origen +"'"
    db.cursor.execute(comando_ciudad_origen)
    id_ciudad_origen = db.cursor.fetchall()[0][0]

if pais_destino != "":
    comando_pais_destino = "SELECT id FROM pais WHERE nombre='"+ pais_destino +"'"
    db.cursor.execute(comando_pais_destino)
    id_pais_destino = db.cursor.fetchall()[0][0]

if ciudad_destino != "":
    comando_ciudad_destino = "SELECT pais FROM ciudad WHERE nombre='"+ ciudad_destino +"'"
    db.cursor.execute(comando_ciudad_destino)
    id_ciudad_destino = db.cursor.fetchall()[0][0]

# Restricciones la descripcion del encargo
if descripcion_encargo == "":
    errores += '<p style="color:red;" ><i> Debe ingresar la descripcion del encargo </i></p>'
elif len(descripcion_encargo)>250:
    errores += '<p style="color:red;" ><i> La descripcion es demasiado larga </i></p>'

# Restricciones de espacio disponible
if espacio == "":
    errores2 += '<p style="color:red;"><i> Debe ingresar la cantidad de espacio del encargo </i></p>'
elif not espacio in Tipos_espacios:
    errores2 += '<p style="color:red;"><i> Este tipo de espacio no esta permitido </i></p>'

# Restricciones kilos disponible
if kilos == "":
    errores += '<p style="color:red;"><i> Debe ingresar la cantidad de kilos del encargo </i></p>'
elif not kilos in Tipos_kilos:
    errores += '<p style="color:red;"><i> Este tipo de kilos no esta permitido </i></p>'

# Restricciones pais de origen
if pais_origen == "":
    errores2 += '<p style="color:red;" ><i> Debe ingresar el pais de origen </i></p>'

# Restricciones ciudad de origen
if ciudad_origen == "":
    errores += '<p style="color:red;"><i> Debe ingresar la ciudad de origen </i></p>'
elif pais_origen != "" and id_pais_origen != id_ciudad_origen:
    errores2 += '<p style="color:red;"><i> La ciudad de origen no coincide con el pais de origen </i></p>'

# Restricciones pais de destino
if pais_destino == "":
    errores2 += '<p style="color:red;"><i> Debe ingresar el pais de destino </i></p>'
elif pais_destino == pais_origen:
    errores += '<p style="color:red;"><i> El pais de destino debe ser distinto al pais de origen </i></p>'

# Restricciones ciudad de destino
if ciudad_destino == "":
    errores += '<p style="color:red;"><i> Debe ingresar la ciudad de destino </i></p>'
elif pais_destino != "" and id_pais_destino != id_ciudad_destino:
    errores2 += '<p style="color:red;"><i> La ciudad de destino no coincide con el pais de destino</i></p>'
elif ciudad_destino == ciudad_origen:
    errores2 += '<p style="color:red;"><i> La ciudad de destino debe ser distinta a la ciudad de origen </i></p>'

# Restricciones archivo foto
if type(foto_encargo)==list or foto_encargo.filename:
    if type(foto_encargo)==list:
        if len(foto_encargo)>3:
            errores2 += '<p style="color:red;" ><i> Hay mas de 3 archivos seleccionados </i></p>'
        else:
            for archivo in foto_encargo:
                tipo = archivo.type
                size = os.fstat(archivo.file.fileno()).st_size
                if tipo not in tipos_soportados:
                    errores2 += '<p style="color:red;"><i> El formato {} del archivo {}no es valido</i></p>'.format(tipo, archivo.filename)
                    break
                elif size > MAX_FILE_SIZE:
                    errores2 += '<p style="color:red;"><i> El archivo {}demasiado grande </i></p>'.format(archivo.filename)
                    break
    else:
        tipo = foto_encargo.type
        size = os.fstat(foto_encargo.file.fileno()).st_size
        if tipo not in tipos_soportados:
            errores2 += '<p style="color:red;"><i> El formato {} del archivo {} no es valido</i></p>'.format(tipo, foto_encargo.filename)
        elif size > MAX_FILE_SIZE:
            errores2 += '<p style="color:red;"><i> El archivo {}demasiado grande </i></p>'.format(foto_encargo.filename)

else:
    errores2 += '<p style="color:red;"><i> Debe ingresar a lo menos una foto</i></p>'

# Restricciones del email
if email_encargo == "":
    errores += '<p style="color:red;"><i> Debe ingresar el email </i></p>'
elif (not re.match(regex_email, email_encargo)):
    errores += '<p style="color:red;"><i> El email no sigue el formato example@email.com </i></p>'

# Restricciones del celular
if celular_encargo != "" and (not re.match(regex_celular, celular_encargo)):
    errores2 += '<p style="color:red;"><i> El celular no sigue el formato +569... </i></p>'

if errores == '' and errores2 == "":
    id1 = "SELECT id FROM ciudad WHERE nombre='"+ ciudad_origen +"'"
    db.cursor.execute(id1)
    id_origen = db.cursor.fetchall()[0][0]

    id2 = "SELECT id FROM ciudad WHERE nombre='" + ciudad_destino + "'"
    db.cursor.execute(id2)
    id_destino = db.cursor.fetchall()[0][0]

    id3 = "SELECT id FROM kilos_encargo WHERE valor='" + kilos + "'"
    db.cursor.execute(id3)
    id_kilos_disponible = db.cursor.fetchall()[0][0]

    id4 = "SELECT id FROM espacio_encargo WHERE valor='" + espacio + "'"
    db.cursor.execute(id4)
    id_espacio_disponible = db.cursor.fetchall()[0][0]

    data = (foto_encargo ,descripcion_encargo, id_espacio_disponible, id_kilos_disponible, id_origen, id_destino, email_encargo, celular_encargo)
    db.save_order(data)
    mensaje = '''
            <div class="py-1 text-center"></div>
            <div class="d-flex align-items-center" >
                <div class="row justify-content-center  vw-100" >
                <div class="alert alert-success col-6" role="alert" style="width:50%;">
                    <h4 class="alert-heading">Encargo agregado con exito!</h4>
                    <p>¡Muchas gracias por agregar tu encargo!</p>
                </div>
                </div>
            </div>
    '''
    with open('../templates/tp_inicio.html','r', encoding="utf-8") as template:
        file = template.read()
        print(file.format('Listado de pedidos pedidos', mensaje), file=utf8stdout)

else:
    with open('../templates/tp_agregar-encargos.html','r', encoding="utf-8") as template: 
        file = template.read()
        print(file.format('Error validación', errores, errores2), file=utf8stdout)


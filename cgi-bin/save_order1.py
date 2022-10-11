#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import sys
import re
import cgitb
from db1 import DB

cgitb.enable()

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)

#Localizamos la base de datos
db = DB('localhost', 'cc500219_u', 'eporttitor', 'cc500219_db')
form = cgi.FieldStorage()

pais_origen = form.getvalue('pais-origen')
ciudad_origen = form.getvalue('ciudad-origen')

pais_destino = form.getvalue('pais-destino')
ciudad_destino = form.getvalue('ciudad-destino')

fecha_ida = form.getvalue('fecha-ida')
fecha_regreso = form.getvalue('fecha-regreso')

espacio_disponibles = form.getvalue('espacio-disponible')
kilos_disponibles = form.getvalue('kilos-disponible')

email = form.getvalue('email')
celular = form.getvalue('celular')

# Validar los campos
errores = ''
errores2 = ''

regex_fecha =  "/^\d{4,4}\-\d{1,2}\-\d{1,2}$/"
regex_fecha = r"^\d{4}([\-/.])(0?[1-9]|1[1-2])\1(3[0-1]|[12][0-9]|0?[1-9])$"
"/([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$/"

Tipos_espacios = ["10x10x10","20x20x20","30x30x30"]
Tipos_kilos = ["200 gr","500 gr","800 gr","1.0 kg","1.5 kg","2.0 kg"]

regex_email = r"/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/"
regex_email = r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$"

regex_celular = r"(\+)?([0-9][-]*){11}$"
regex_celular = r"^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$/"
regex_celular = r"^(\(?\+[\d]{1,3}\)?)\s?([\d][\s\.-]?){8,9}$"


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

# Restricciones pais de origen
if pais_origen == "":
    errores += '<p style="color:red;" ><i> Debe ingresar el pais de origen </i></p>'

# Restricciones ciudad de origen
if ciudad_origen == "" :
    errores2 += '<p style="color:red;"><i> Debe ingresar la ciudad de origen </i></p>'
elif pais_origen != "" and id_pais_origen != id_ciudad_origen:
    errores2 += '<p style="color:red;"><i> La ciudad de origen no coincide con el pais de origen </i></p>'

# Restricciones pais de destino
if pais_destino == "":
    errores += '<p style="color:red;"><i> Debe ingresar el pais de destino </i></p>'
elif pais_destino == pais_origen:
    errores += '<p style="color:red;"><i> El pais de destino debe ser distinto al pais de origen </i></p>'

# Restricciones ciudad de destino
if ciudad_destino == "":
    errores2 += '<p style="color:red;"><i> Debe ingresar la ciudad de destino </i></p>'
elif pais_destino != "" and id_pais_destino != id_ciudad_destino:
    errores2 += '<p style="color:red;"><i> La ciudad de destino no coincide con el pais de destino</i></p>'
elif ciudad_destino == ciudad_origen:
    errores2 += '<p style="color:red;"><i> La ciudad de destino debe ser distinta a la ciudad de origen </i></p>'

# Restricciones fecha de ida 
if fecha_ida == "":
    errores += '<p style="color:red;"><i> Debe ingresar la fecha de ida </i></p>'
elif (not re.match(regex_fecha, fecha_ida)):
    errores += '<p style="color:red;"><i> La fecha de ida no sigue el formato año-mes-dia </i></p>'

# Restricciones fecha de regreso
if fecha_regreso == "":
    errores2 += '<p style="color:red;"><i> Debe ingresar la fecha de regreso </i></p>'
elif (not re.match(regex_fecha, fecha_regreso)):
    errores2 += '<p style="color:red;"><i> La fecha de regreso no sigue el formato año-mes-dia </i></p>'
elif fecha_regreso <= fecha_ida:
    errores2 += '<p style="color:red;"><i> La fecha de regreso debe ser posterior a la fecha de ida </i></p>'

# Restricciones de espacio disponible
if espacio_disponibles == "":
    errores += '<p style="color:red;"><i> Debe ingresar la cantidad de espacio disponible </i></p>'
elif not espacio_disponibles in Tipos_espacios:
    errores += '<p style="color:red;"><i> Este tipo de espacio no esta permitido </i></p>'

# Restricciones kilos disponible
if kilos_disponibles == "":
    errores2 += '<p style="color:red;"><i> Debe ingresar la cantidad de kilos disponibles </i></p>'
elif not kilos_disponibles in Tipos_kilos:
    errores2 += '<p style="color:red;"><i> Este tipo de kilos no esta permitido </i></p>'

# Restricciones del email
if email == "":
    errores += '<p style="color:red;"><i> Debe ingresar el email </i></p>'
elif (not re.match(regex_email, email)):
    errores += '<p style="color:red;"><i> El email no sigue el formato example@email.com </i></p>'

# Restricciones del celular
if celular != "" and (not re.match(regex_celular, celular)):
    errores2 += '<p style="color:red;"><i> El celular no sigue el formato +56... </i></p>'

if errores == '' and errores2 == "":
    id1 = "SELECT id FROM ciudad WHERE nombre='"+ ciudad_origen +"'"
    db.cursor.execute(id1)
    id_origen = db.cursor.fetchall()[0][0]

    id2 = "SELECT id FROM ciudad WHERE nombre='" + ciudad_destino + "'"
    db.cursor.execute(id2)
    id_destino = db.cursor.fetchall()[0][0]

    id3 = f'''SELECT id FROM kilos_encargo WHERE valor="{kilos_disponibles}"'''
    db.cursor.execute(id3)
    id_kilos_disponible = db.cursor.fetchall()[0][0]

    id4 = f'''SELECT id FROM espacio_encargo WHERE valor="{espacio_disponibles}"'''
    db.cursor.execute(id4)
    id_espacio_disponible = db.cursor.fetchall()[0][0]

    data = (id_origen, id_destino, fecha_ida, fecha_regreso, id_kilos_disponible, id_espacio_disponible, email, celular)
    db.save_order(data)
    mensaje = '''
            <div class="py-1 text-center"></div>
            <div class="d-flex align-items-center" >
                <div class="row justify-content-center  vw-100" >
                <div class="alert alert-success col-6" role="alert" style="width:50%;">
                    <h4 class="alert-heading">Viaje agregado con exito!</h4>
                    <p>¡Muchas gracias por agregar tu viaje!</p>
                </div>
                </div>
            </div>
    '''
    with open('../templates/tp_inicio.html','r', encoding="utf-8") as template:
        file = template.read()
        print(file.format('Listado de pedidos pedidos', mensaje), file=utf8stdout)

else:
    with open('../templates/tp_agregar-viaje.html','r', encoding="utf-8") as template: 
        file = template.read()
        print(file.format('Error validación', errores, errores2), file=utf8stdout)


#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cgi
from db1 import DB

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)

#Rellenar acá con datos que faltan.
db = DB('localhost', 'cc500219_u', 'eporttitor', 'cc500219_db')
args = cgi.FieldStorage()

id = args.getvalue('id')
data = db.get_viaje(id)


comando1 = "SELECT nombre FROM ciudad WHERE id='"+ str(data[0][1]) + "'"
db.cursor.execute(comando1)
origen = db.cursor.fetchall()[0][0]

comando2 = "SELECT nombre FROM ciudad WHERE id='"+ str(data[0][2]) +"'"
db.cursor.execute(comando2)
destino = db.cursor.fetchall()[0][0]

comando3 = "SELECT valor FROM espacio_encargo WHERE id="+ str(data[0][6])
db.cursor.execute(comando3)
espacio = db.cursor.fetchall()[0][0]

comando4 = "SELECT valor FROM kilos_encargo WHERE id="+ str(data[0][5])
db.cursor.execute(comando4)
kilos = db.cursor.fetchall()[0][0]

if (id != None):
    informacion = f'''
    <div><a href="ver-viajes.py">/ver-viajes/</a></div>
        <div>
            <div class="py-1 text-center"></div>
            <h2 id="foto1">#{data[0][0]}</h2>
            <div class="bloques" >
                <img src="../Tarea1/envio-03.jpg" width="640" height="480" alt="">
            </div>
            <div class="bloques" style="max-width:400px;">
                <div class="py-4 text-center"></div>
                <h4>Detalle</h4>
                <div class="py-1 text-center"></div>
                <div><p><b>Origen:</b> {origen}</p></div>
                <div><p><b>Destino: </b>  {destino}</p></div>
                <div><p><b>Fecha de ida:</b>  {str(data[0][3])[:10]}</p></div>
                <div><p><b>Fecha de llegada: </b>  {str(data[0][4])[:10]}</p></div>
                <div><p><b>Espacio: </b>  {espacio}</p></div>
                <div><p><b>Kilos: </b>  {kilos}</p></div>
                <div><p><b>Email:</b>  {data[0][7]}</p></div>
                <div><p><b>Telefono:</b>  {data[0][8]} </p></div>
            </div>
        </div>

        <div class="py-4 text-center"></div>
        <div style="text-align:center;"><button type="button" class="btn btn-lg btn-outline-dark" onclick="location.href='ver-viajes.py?page=0 '" >Regresar</button></div>
        <div class="py-4 text-center"></div>
    '''

else: 
    tabla = '''
            <div class="d-flex align-items-center">
                <div class="container p-3 my-3 border bg-light text-center">
                    Falta agregar parámetro id en la url!
                </div>
            </div>
    '''

with open('../templates/tp_informacion-viajes.html','r', encoding="utf-8") as template:
    file = template.read()
    print(file.format(informacion), file=utf8stdout)
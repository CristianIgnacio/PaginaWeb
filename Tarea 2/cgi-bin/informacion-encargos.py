#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cgi
from db2 import DB

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)

#Rellenar acá con datos que faltan.
db = DB('localhost', 'cc500219_u', 'eporttitor', 'cc500219_db')
args = cgi.FieldStorage()

id = args.getvalue('id')
data = db.get_encargo(id)

#(id, descripcion, espacio, kilos, origen, destino, email_encargo, celular_encargo)

comando1 = "SELECT nombre FROM ciudad WHERE id='"+ str(data[0][4]) + "'"
db.cursor.execute(comando1)
origen = db.cursor.fetchall()[0][0]

comando2 = "SELECT nombre FROM ciudad WHERE id='"+ str(data[0][5]) +"'"
db.cursor.execute(comando2)
destino = db.cursor.fetchall()[0][0]

comando3 = "SELECT valor FROM espacio_encargo WHERE id="+ str(data[0][2])
db.cursor.execute(comando3)
espacio = db.cursor.fetchall()[0][0]

comando4 = "SELECT valor FROM kilos_encargo WHERE id="+ str(data[0][3])
db.cursor.execute(comando4)
kilos = db.cursor.fetchall()[0][0]

comando5 = "SELECT ruta_archivo FROM foto WHERE encargo_id="+ str(id)
db.cursor.execute(comando5)
foto = db.cursor.fetchall()


informacion = ""

if (id != None):
    informacion +='''
        <script>
            function Change(){
    '''
    for i in range(len(foto)):
        informacion += f'''
            document.getElementById("{i+1}").height="1024";
            document.getElementById("{i+1}").width="1280";
        '''
    informacion += '''
            document.getElementById("a").style.marginLeft="0";
            document.getElementById("a").style.marginRight="0";
            document.getElementById("carouselExampleIndicators").style.maxWidth="1280px";
            }
            function Revert()
            {
    '''
    for i in range(len(foto)):
        informacion += f'''
            document.getElementById("{i+1}").height="480";
            document.getElementById("{i+1}").width="640";
        '''
    informacion += '''
            document.getElementById("a").style.marginLeft="auto";
            document.getElementById("a").style.marginRight="auto";
            document.getElementById("carouselExampleIndicators").style.maxWidth="640px";
            }
        </script>
    '''
    informacion += f'''
        <div>
            <div class="py-1 text-center"></div>
            <h2 id="foto1">#{id}</h2>
            <div class="bloques" id="hola">
            <div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel" style="max-width:640px;">
                <ol class="carousel-indicators">
    '''
    for i in range(len(foto)):
        if(i==0):   
            informacion += '''' <li data-target="#carouselExampleIndicators" data-slide-to="0" class="active"></li>''' 
        else:
            informacion += f'''  <li data-target="#carouselExampleIndicators" data-slide-to="{i}"></li>'''
    informacion += '''
                </ol>
                <div class="carousel-inner">
    '''
    for i in range(len(foto)):
        if i==0:
            informacion += f'''
                    <div class="carousel-item active">
                    <img class="d-block " id="1" src="../media/{foto[0][0]}" alt="First slide" width="640" height="480" onclick="Change()" ondblclick="Revert()">
                    </div>
            '''
        else:
            informacion += f'''
                    <div class="carousel-item">
                    <img class="d-block" id="{i+1}"  src="../media/{foto[i][0]}" alt="Second slide" width="640" height="480" onclick="Change()" ondblclick="Revert()">
                    </div>
            '''
    informacion += f'''
                </div>
                <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="sr-only">Previous</span>
                </a>
                <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="sr-only">Next</span>
                </a>
            </div>            
        </div>
            <div class="bloques" style="max-width:400px;">
                <div class="py-2 text-center"></div>
                <h4>Detalle</h4>
                <div class="py-1 text-center"></div>
                <div><p><b>Origen:</b> {origen}</p></div>
                <div><p><b>Destino: </b> {destino}</p></div>
                <div><p><b>Espacio: </b> {espacio}</p></div>
                <div><p><b>Kilos: </b> {kilos}</p></div>
                <div><p><b>Email: </b> {data[0][6]}</p></div>
                <div><p><b>Telefono: </b> {data[0][7]}</p></div>
                <div><p><b>Descripcion: </b>{data[0][1]}</p></div>

            </div>
        </div>
        <div class="py-4 text-center"></div>
        <div style="text-align:center;"><button type="button" class="btn btn-lg btn-outline-dark" onclick="location.href='ver-encargos.py?page=0'">Regresar</button></div>
        <div class="py-4 text-center"></div>
    '''
else: 
    informacion = '''
            <div class="d-flex align-items-center">
                <div class="container p-3 my-3 border bg-light text-center">
                    Falta agregar parámetro id en la url!
                </div>
            </div>
    '''

with open('../templates/tp_informacion-encargos.html','r', encoding="utf-8") as template:
    file = template.read()
    print(file.format(informacion), file=utf8stdout)
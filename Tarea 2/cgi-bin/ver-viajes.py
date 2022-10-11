#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import sys
import cgitb
import math
from db1 import DB

cgitb.enable()

def tuplas(list, text,db):
    for i in list:
        comando1 = "SELECT nombre FROM ciudad WHERE id='"+ str(i[1]) + "'"
        db.cursor.execute(comando1)
        origen = db.cursor.fetchall()[0][0]

        comando2 = "SELECT nombre FROM ciudad WHERE id='"+ str(i[2]) +"'"
        db.cursor.execute(comando2)
        destino = db.cursor.fetchall()[0][0]

        comando3 = f"SELECT valor FROM kilos_encargo WHERE id={i[5]}"
        db.cursor.execute(comando3)
        kilos = db.cursor.fetchall()[0][0]

        comando4 = f"SELECT valor FROM espacio_encargo WHERE id={i[6]}"
        db.cursor.execute(comando4)
        espacio = db.cursor.fetchall()[0][0]

        text += f"""
            <tbody>
            <tr>
                <th scope="col" class="align-middle">{i[0]}</th>
                <td class="align-middle">{origen}</td>
                <td class="align-middle">{destino}</td>
                <td class="align-middle">{str(i[3])[:10]}</td>
                <td class="align-middle">{str(i[4])[:10]}</td>
                <td class="align-middle">{kilos}</td>
                <td class="align-middle">{espacio}</td>
                <td class="align-middle">{i[7]}</td>
                <td class="align-middle"><button type="button" class="btn btn-outline-dark" onclick="location.href='informacion-viajes.py?id={i[0]}'">ir</button></td>

            </tr>
            </tbody>
        """
    return text

def pagination(num, page):
    filas = num + 1
    paginas = math.ceil(filas/5)
    page +=1
    if(page == 1):
        text = '''
            <ul class="pagination justify-content-center">
              <li class="page-item disabled">
                <span class="page-link">Previous</span>
              </li>
        '''
    else:
        text = f'''
            <ul class="pagination justify-content-center">
              <li class="page-item ">
                <a class="page-link" href="ver-viajes.py?page={page-2}">Previus</a>
              </li>
        '''
    for i in range(paginas):
        p = i +1
        if p!=page:
            text += f'''
                <li class="page-item"><a class="page-link" href="ver-viajes.py?page={p-1}" style=>{p}</a></li>
            '''
        else:
            text += f'''
                <li class="page-item active">
                <span class="page-link">
                  {p}
                  <span class="sr-only">(current)</span>
                </span>
                </li>
            '''
    if paginas==page:
        text +='''
            <li class="page-item disabled" >
                <span class="page-link">Next</span>
                </li>
            </ul>
        ''' 
    else:
        text += f'''
            <li class="page-item">
                <a class="page-link" href="ver-viajes.py?page={page}">Next</a>
              </li>
            </ul>
        ''' 
    return text

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)

db = DB('localhost', 'cc500219_u', 'eporttitor', 'cc500219_db')
form = cgi.FieldStorage()

page = form.getvalue('page')
pagina = page
if int(page)>0:
    pagina = int(page)*5-1

primeros5 = f"SELECT id, origen, destino, fecha_ida, fecha_regreso, kilos_disponible, espacio_disponible, email_viajero, celular_viajero FROM viaje ORDER BY id ASC LIMIT {pagina},5"
db.cursor.execute(primeros5)
ids_primeros5 = db.cursor.fetchall()
codigo = ''
codigo = tuplas(ids_primeros5, codigo, db)

comandonumero = "SELECT COUNT(*) AS conteo FROM viaje"
db.cursor.execute(comandonumero)
cantidad = db.cursor.fetchall()[0][0]
codigo2 = ""
codigo2 = pagination(int(cantidad), int(page))

with open('../templates/tp_ver-viajes.html','r', encoding="utf-8") as template:
    file = template.read()
    print(file.format(codigo, codigo2), file=utf8stdout)

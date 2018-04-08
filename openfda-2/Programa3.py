# coding=utf-8
import http.client
import json
#Puesto que tengo que hallar todos los fabricantes de aspirnina, hay 858 casos relacionados con las aspirinas y el propio servidor dice que el
#parámetro de búsqueda "limit" no puede exceder de 100 es necesario hacer varias peticiones al servidor para obtener todos los datos.
#Dicho esto ire explicando paso a paso lo que he hecho.
#Esta lista la creo para ir guardando en ella cada fabricante de aspirinas NUEVO que encuentro
fabricanteslista=[]
#Me conecto al servidor
conn = http.client.HTTPSConnection("api.fda.gov")
#Mi variable skip me sirve para regular las veces que me conecto al servidor, es un parametro de búsqueda que omite el numero de registros que
#le pases.De modo que primero cojo 100 registros y cuando me vuelva a conectar al servidor lo hago con el parametro de busqeda skip(anterior)+100
#y asi el servidor me enviará los 100 siguientes. Por ello en .request voy modificando la URL con la variable skip.
skip=0
#Lo meto todo en un bucle para que me repita el proceso hasta que se de una determinada condición que luego explicaré
while True:
    conn.request("GET","https://api.fda.gov/drug/label.json?search=openfda.substance_name:%22ASPIRIN%22&limit=100&skip="+str(skip), None)
    #Leo la respuesta que ha sido enciada por el servidor e imprimo su linea de estado para ver si todo ha ido bien, además al lado de la misma
    #indico el valor de skip en ese momento para que el usuario siga más o menos en que punto esta el programa.
    r1 = conn.getresponse()
    print(r1.status, r1.reason, "(for query parameter skip=%i)"% skip)
    #las dos lineas siguientes ya han sido explicadas en la practica anterior y es exactamente lo mismo
    recurso_bytes = r1.read().decode("utf-8")
    recurso = json.loads(recurso_bytes)
    #A continuación, itero cada uno de los registro que me ha enviado el servidor par ese skip en concreto e introduzco el nombre del fabricante
    #de la aspirina en mi variable fabricante, la cual iré usando para añadir o no elementos a la lista según me convenga
    for valor in range(len(recurso["results"])):
        fabricante=recurso["results"][valor]["openfda"]["manufacturer_name"][0]
        #si el fabricante ya está en la lista no lo añade
        if fabricante in fabricanteslista:
            pass
        #de lo contrario, si lo hace.
        else:
            fabricanteslista.append(fabricante)
    #Aqui llegamos al código que determina si se repite o no el bucle, en la variable total_casos se almacena el numero total de registros para esa busqueda
    total_casos=recurso["meta"]["results"]["total"]
    #De modo que si mi skip actual está por debajo del numero total de registro le sumo otros 100 puesto que aún quedan casos por consultar
    if skip < total_casos:
        skip+=100
        #de lo contrario ya he terminado y salgo del bucle
        if skip>=total_casos:
            break
#Ahora ordenaré con sorted() mi lista de fabricantes porque me será más útil ordenada y voy uno a uno imprimiento por pantalla cada uno
#de los fabricantes de aspirina y además indico el numero de fabricantes que hay.
lista_ordenada=sorted(fabricanteslista)
print("\n   Number of manufacturers:",len(lista_ordenada))
print("   Total records for this search:", total_casos)
for i in lista_ordenada:
    print("     ",i)

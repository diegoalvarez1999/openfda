import http.client
import json
#Me conecto con el servidor. En la misma URL tengo IP:PORT
conn = http.client.HTTPSConnection("api.fda.gov")
#A partir de ahora "conn" es como la clase HTTPSConnection y utilizare sus objetos de la forma: conn.funcion()
#Con .request, solicito al servidor, api.fda.gov, mediante el metodo GET que me envie el recurso /drug/label.json
conn.request("GET","https://api.fda.gov/drug/label.json",body=None)
#Ahora leo el mensaje respuesta que me ha enviado el servidor con .getresponse()
r1 = conn.getresponse()
#Imprimo la linea de estado de la respuesta para ver que todo OK, si el estado de respuesta es 200 OK
#ignifica que el recurso ha sido recuperado y se transmite en el cuerpo del mensaje
print(r1.status, r1.reason)
#Ahora leo el recurso y he de pasarlo a str con decode porque es enviado en bytes
recurso_bytes = r1.read().decode("utf-8")
#Una vez hecho esto obtengo un JSON, que para python es simplemente un str, y de un str, nos sería muy dificil extraer lo que pide la practica
#Una vez obtenido lo que quiero, cierro la conexion con el servidor
conn.close()

#Esto no es necesario salvo que se quiera guardar el JSON enviado por el servidor en el ordenador:
with open("jsonfile", "w") as f:
    f.write(recurso_bytes)

#Me es necesario usar la función .loads() que lo que hace es decodificarme la cadena (str) JSON que hay guardada en la variable
#recurso_bytes y me la convierte en un objeto python de tipo dict
recurso=json.loads(recurso_bytes)
#Una vez aqui, me he ido a Firefox y he introducido https://api.fda.gov/drug/label.json, para observar el formato más comodamente.
#Puesto que todo lo de esa URL lo he convertido en un diccionario(recurso), puedo ir iterando sobre sus claves, llegando a la conclusión de que
#los datos que me intersan está en una de las dos claves principales(meta y results), en results y a su vez englobados todos ellos en la clave 0.
#Por eso me creo una variable que contenga toda la información de mi interes. Que es todo aquello englobado en 0
infomedica=recurso["results"][0]
#Una vez hecho esto, ya lo tengo todo, infomedica(la parte que me interesa del JSON)es un diccionario reducido de mi diccionario principal(recurso)
#Ahora, simplemente le pedire a python que me imprima el valor de la clave que me interesa.
#sabiendo que en un diccionario python se obtiene el valor pasandole la clave entre corchetes: diccionario[clave] me da [valor]
#De este modo, guiándome en el navegador voy identando en mi diccionario hasta llegar a los datos que busco
print ("ID: ",infomedica["id"])
#Por ejemplo para el proposito, veo en el formato JSON del navegador que se encuentra en la seccion "purpose"(clave) que engloba a su vez
#a "0" que es la clave cuyo valor es mi dato buscado, el proposito.
print ("PROPOSITO: ",infomedica["purpose"][0])
print ("FABRICANTE: ",infomedica["openfda"]["manufacturer_name"][0])

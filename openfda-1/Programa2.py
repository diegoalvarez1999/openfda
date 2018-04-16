# coding=utf-8
import http.client
import json

# Este programa 2 lo llevaré a cabo de forma exactamente igual que el 1, pues lo que tenemos que hacer es exactamente lo mismo,
# me conecto al servidor, utilizo la función .request() del módulo http.client para solicitar al servidor lo que quiero, para ello utilizo
# el método GET, leo el mensaje respuesta con la función .getresponse(), imprimo la linea de estado de respuesta para ver si ha tenido éxito
# la petición, decofifico la respuesta para obtener un mensaje legible en "recurso_bytes" y creo un objeto Python como el diccionario
# "recurso" para poder trabajar con él facilmente con la función .loads().
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "https://api.fda.gov/drug/label.json?limit=10", None)

r1 = conn.getresponse()
print(r1.status, r1.reason)
# recurso_bytes es un string
recurso_bytes = r1.read().decode("utf-8")
# Cierro la conexión
conn.close()
# Creo mi diccionario
recurso = json.loads(recurso_bytes)

# Una vez que tengo el diccionario (recurso) creado como en el programa 1 ire identando en él hasta conseguir el id de cada medicamento.
# Tengo que tener en cuenta que esta vez para una de mis claves principales, "results" en vez tener solo un valor ("0") como en el ej anterior
# ahora tengo 10 valores (del 0 al 9) y cada uno de esos valores es un medicamento, por tanto por cada uno de ellos tendré que encontrar el id
# e imprimirlo.
# Es obvio que la mejor forma de hacer esto es mediante un bucle "for" que vaya identando uno a uno todos los elementos que le indique.
# Previamente me he hecho un print(range(len(recurso["results"]))) para cerciorarme de que el numero de valores que tiene recurso para "results" es
# 10. Ahora podría ir iterando sobre cada uno de esos valores, yyy dentro de cada uno de esos valores buscar el id e imprimirlo por pantalla.
for valor in (range(len(recurso["results"]))):
    print("ID: ", recurso["results"][valor]["id"])

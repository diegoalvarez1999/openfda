#importamos los módulos que python nos ofrece para crear un servidor
import http.server
import socketserver
import http.client
import json

PORT = 8005

#ahora creamos nuestro propio manejador (para que gestione la peteción del cliente como queramos) a partir de uno básico que nos sirve de base.
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # GET. Este metodo se invoca automaticamente cada vez que hay una
    # peticion GET por HTTP. El recurso que nos solicitan se encuentra
    # en self.path
    def do_GET(self):
        # Indicamos al cliente que su petición ha sido procesada correctamente
        self.send_response(200)
        # En las siguientes lineas de la respuesta colocamos las cabeceras necesarias para que el cliente entienda el contenido que le
        # enviamos (que sera HTML)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        #DESPUES DE ESTO DEFINIMOS LO QUE QUERAMOS HACER CON LA PETICIÓN
        list_genericname = []
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "https://api.fda.gov/drug/label.json?limit=10", None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        recurso_bytes = r1.read().decode("utf-8")
        conn.close()
        recurso = json.loads(recurso_bytes)

        #ahora establezo el codigo que procesara la petición, iterando sobre recurso en cada uno de los valores hasta llegar a generic_name
        #puede que algun registro no presente generic_name por cualquier motivo, por eso tratamos esa posibilidad con if.
        #Todo lo que hay dentro de bucle for se nos presentará en la terminal al ejecutar el programa, para que aparezca en el navegador tenemos
        #que  pasarlo a formato HTML.
        for valor in range(len(recurso["results"])):
            if recurso["results"][valor]["openfda"]:
                generic_name= recurso["results"][valor]["openfda"]["generic_name"][0]
                print("("+str(valor)+")"+"Nombre medicamento:", generic_name)
                list_genericname.append(generic_name)

        #este contenido se presentara en el navegador, lo pasamos a HTML siguiendo el protocolo html:
        contenido= """<html><body>"""
        #ahora, por cada valor en mi list_genericname lo añado a contenido (mi html) y con "<br>" salto de linea para escribir el siguiente
        for i in list_genericname:
            contenido += i+ "<br>"
        contenido += """</html></body>"""
        #esta linea me permite mostrar el contenido, lo que haga el manejador con la petición, en la pantalla del navegador, en HTML
        self.wfile.write(bytes(contenido, "utf8"))
        return


# El servidor comienza a aqui
# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler
#definimos nuetro servidor indicando el puerto y el manejador que gestionara las peticiones(testHTTPRequestHandler, el cual hemos definido ya)
httpd = socketserver.TCPServer(("", PORT), Handler)
print("servidor en puerto", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")


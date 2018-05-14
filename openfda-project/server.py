import http.server
import http.client
import json
import socketserver

PORT=8000
INDEX_FILE= "index.html"
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # gestiono todas las posiples URL de openfda que me harán falta
    OPENFDA_SERVER="api.fda.gov"
    OPENFDA_ENDPOINT="/drug/label.json"
    OPENFDA_DRUG_IN_ENDPOINT='&search=active_ingredient:'
    OPENFDA_COMPANY_IN_ENDPOINT='&search=manufacturer_name:'

    #defino la pagina pagina_principal, que será mi archivo index.html
    def pagina_principal(self):
        with open(INDEX_FILE, "r") as f:
            index_html = f.read()

        return index_html

#esta funcio me servira para pasar  a HTML las listas que vaya creando de los datos que me pasa opnfda
    def dame_web(self, lista):
        lista_html = """
        <html>
            <head>
                <title>OpenFDA Results</title>
            </head>
            <body>
                <ul>"""
        for item in lista:
            lista_html += "<li>" + item + "</li>"

        lista_html += """
                </ul>
                <a href="/">Home</a>
            </body>
        </html>"""
        return lista_html

    #bien, hasta aqui tengo tan solo herramientas para la visualizacion, ahora necesito herramientas que me permitan obtener los datos que busco
    #esta función será la que me conecte al servidor de openfda y me pase sus datos a un formajo python
    def dame_resultados(self, limit=10):
        conn = http.client.HTTPSConnection(self.OPENFDA_SERVER)
        conn.request("GET", self.OPENFDA_ENDPOINT + "?limit="+str(limit))
        print (self.OPENFDA_ENDPOINT + "?limit="+str(limit))
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        recurso_bytes = r1.read().decode("utf8")
        conn.close()
        recurso_dicc= json.loads(recurso_bytes)
        resultados = recurso_dicc['results']
        return resultados

    #Ahora mediante do_GET(), gestiono la respuesta de MI API REST
    def do_GET(self):
        #separo la barra de estado
        recurso_list = self.path.split("?")
        if len(recurso_list) > 1:
            parametros = recurso_list[1]
        else:
            parametros = ""

        contenido_html=""
        #searchDrug?active=farmaco&limit=10
        #listdrugs?limit=10
        #paraetros= active_ingredient=farmaco&limit=10 o limit=10
        #split_parametros=[active_ingredient=farmaco, limit=10]
        #split_buscado= [active_ingredient, farmaco, limit, 10]
        # las siguientes lineas, me serviran para establecer el limite de busqueda en mi api
        if parametros:
            if "&" in parametros:
                split_parametros = parametros.split("&")
                for element in split_parametros:
                    split_buscado= element.split("=")
                    if split_buscado[0]=="limit":
                        limit=int(split_buscado[1])
            else:
                split_limit = parametros.split("=")
                if split_limit[0] == "limit":
                    limit = int(split_limit[1])

            print("Limit: {}".format(limit))
        else:
            print("SIN PARAMETROS")


        self.send_response(200)
        # envio las cabeceras
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        #aqui gestiono los posibles recursos que puede ofrecer mi api rest dependiendo del directorio solicitado
        #el recurso que solicita el cliente a la api rest esta en self.path
        if self.path=='/':#página índice
            contenido_html=self.pagina_principal()

        elif "listDrugs" in self.path:
            farmacos = []#creo esta lista para luego poder pasar sus elementos a html con mi funcion dame_web
            resultados = self.dame_resultados(limit)
            for valor in resultados:
                if ('generic_name' in valor['openfda']):
                    farmacos.append (valor['openfda']['generic_name'][0])
                else:
                    farmacos.append(' DESCONOCIDO')
            contenido_html = self.dame_web (farmacos)

        elif "listCompanies" in self.path:
            fabricantes = []
            resultados = self.dame_resultados(limit)
            for valor in resultados:
                if ('manufacturer_name' in valor['openfda']):
                    fabricantes.append (valor['openfda']['manufacturer_name'][0])
                else:
                    fabricantes.append(' DESCONOCIDO')
            contenido_html = self.dame_web(fabricantes)

        elif 'listWarnings' in self.path:
            warnings = []
            resultados = self.dame_resultados (limit)
            for valor in resultados:
                if ('warnings' in valor):
                    warnings.append (valor['warnings'][0])
                else:
                    warnings.append('Desconocido')
            contenido_html = self.dame_web(warnings)

        elif 'searchDrug' in self.path:#no puedo ponerlo como self.path==, porque despues de searchDrug hay más cosas
            #EJ: path =/searchDrug?active_ingredient=silicea&limit=3
            farmaco_y_limite=self.path.split('=')[1]#separo para saber cual es el fármaco de interes que introduce el usuario y asi poder completar
            farmaco=farmaco_y_limite.split("&")[0]
            #la URL de petición para OpenFDA
            medicamentos = []#de nuevo, creo una lista donde voy añadiendo lo que busco y luego uso dame_web
            conn = http.client.HTTPSConnection(self.OPENFDA_SERVER)
            conn.request("GET", self.OPENFDA_ENDPOINT + "?limit="+str(limit) + self.OPENFDA_DRUG_IN_ENDPOINT + farmaco)
            print(self.OPENFDA_ENDPOINT + "?limit="+str(limit) + self.OPENFDA_DRUG_IN_ENDPOINT + farmaco)
            r1 = conn.getresponse()
            recurso_bytes = r1.read().decode("utf8")
            recurso_dicc = json.loads(recurso_bytes)
            try:
                for valor in recurso_dicc['results']:
                    if ('generic_name' in valor['openfda']):
                        medicamentos.append(valor['openfda']['generic_name'][0])
                    else:
                        medicamentos.append(' DESCONOCIDO')
            except KeyError:
                self.send_error(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("I don't know '{}'.".format(self.path).encode())

            contenido_html = self.dame_web(medicamentos)

        elif 'searchCompany' in self.path:
            empresa_y_limite=self.path.split('=')[1]
            empresa=empresa_y_limite.split("&")[0]
            empresas = []
            conn = http.client.HTTPSConnection(self.OPENFDA_SERVER)
            conn.request("GET", self.OPENFDA_ENDPOINT + "?limit=" + str(limit) + self.OPENFDA_COMPANY_IN_ENDPOINT + empresa)
            r1 = conn.getresponse()
            recurso_bytes = r1.read().decode("utf8")
            recurso_dicc = json.loads(recurso_bytes)
            try:
                for valor in recurso_dicc['results']:
                    if ('manufacturer_name' in valor['openfda']):
                        empresas.append(valor['openfda']['manufacturer_name'][0])
                    else:
                        empresas.append(' DESCONOCIDO')
            except KeyError:
                self.send_error(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("I don't know '{}'.".format(self.path).encode())
            contenido_html = self.dame_web(empresas)

        elif 'redirect' in self.path:
            self.send_response(301)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()
        elif 'secret' in self.path:
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        else:
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())

        self.wfile.write(bytes(contenido_html, "utf8"))

socketserver.TCPServer.allow_reuse_address= True
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

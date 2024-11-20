from http.server import HTTPServer, BaseHTTPRequestHandler
from email.parser import BytesParser
from email.policy import default

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Obtiene la longitud del contenido
        content_length = int(self.headers['Content-Length'])
        # Lee los datos enviados en el POST
        post_data = self.rfile.read(content_length)

        # Usa el parser de email para manejar multipart/form-data
        headers = {'Content-Type': self.headers['Content-Type']}
        message = BytesParser(policy=default).parsebytes(
            b'\r\n'.join(f"{k}: {v}".encode() for k, v in headers.items()) + b'\r\n\r\n' + post_data
        )

        # Variable para almacenar el archivo si se encuentra
        file_data = None

        # Mensaje de depuración para confirmar el contenido recibido
        print("Partes encontradas en el payload:")

        # Recorre las partes del payload buscando el archivo
        for part in message.iter_parts():
            disposition = part.get("Content-Disposition", "")
            if disposition and "form-data" in disposition:
                name_param = part.get_param('name', header="Content-Disposition")
                if name_param == "data":
                    file_data = part.get_payload(decode=True)
                    print("Archivo encontrado y decodificado.")
                    break

        # Guarda el archivo si se recibió correctamente
        if file_data:
            with open("uploaded_file.sqlite", "wb") as f:
                f.write(file_data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Archivo recibido con exito")
        else:
            print("No se encontro ningun archivo en la carga.")
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No se recibio ningun archivo")

    def do_GET(self):
        # Respuesta simple para probar el funcionamiento del servidor
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Servidor activo y listo para recibir archivos.")

if __name__ == "__main__":
    server_address = ('', 80)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Servidor iniciado en el puerto 80...")
    httpd.serve_forever()

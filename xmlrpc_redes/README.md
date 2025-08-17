# 🖥️ Servidor y Cliente RPC con Sockets TCP en Python

Este proyecto implementa un **servidor** y un **cliente** que se comunican mediante **sockets TCP**.  
La idea es simular un sistema de **Remote Procedure Call (RPC)**: el cliente puede invocar funciones remotas en el servidor enviando solicitudes en formato XML (aún no implementado en detalle).

---

## 📌 Código Principal

```python
import socket
import utils  # Módulo auxiliar para procesar XML (no incluido aquí)

# =========================
# Clase Server
# =========================
class Server:
    server_welcoming_socket = None
    my_address = None
    my_port = None
    procedures = {}  # Diccionario de métodos disponibles

    def __init__(self, address, port):
        """Inicializa el servidor con IP y puerto."""
        self.server_welcoming_socket = socket(AF_INET, SOCK_STREAM)  # Socket TCP
        self.server_welcoming_socket.bind((address, port))
        self.my_address, self.my_port = self.server_welcoming_socket.getsockname()
        print(f'Servidor creado con IP: {self.my_address} y puerto: {self.my_port}')
    
    def add_method(self, method):
        """Agrega un procedimiento remoto al diccionario de métodos."""
        if method in self.procedures:
            self.procedures[method.__name__] = method
            print('El procedimiento ya existía y ha sido actualizado.')
        else:
            self.procedures[method].__name__ = method
            print('El procedimiento ha sido agregado correctamente.')

    def serve(self):
        """Bucle principal para aceptar y procesar conexiones de clientes."""
        while True:
            self.server_welcoming_socket.listen(1)  # Cola máxima de 1 conexión pendiente
            print('El servidor está listo para recibir.')
            connection_socket, cl_address_port = self.server_welcoming_socket.accept()
            print(f'Conexión establecida con {cl_address_port}')
            
            request_in_xml = connection_socket.recv().decode()  # Recibe solicitud en XML
            # TODO: Procesar XML
            # TODO: Ejecutar función con sus parámetros
            # TODO: Convertir resultado a XML
            
            response_in_xml = None
            connection_socket.send(response_in_xml)
            print(f'Resultado enviado hacia el cliente {cl_address_port}')
            connection_socket.close()  # Conexión no persistente

# =========================
# Clase Connection
# =========================
class Connection:
    client_socket = None
    sv_address = None
    sv_port = None
    request_in_xml = None
    response_in_xml = None

    def __init__(self, cl_socket, sv_address, sv_port):
        """Inicializa la conexión de cliente hacia el servidor."""
        self.client_socket = cl_socket
        self.sv_address = sv_address
        self.sv_port = sv_port
        self.client_socket.connect((self.sv_address, self.sv_port))
        print(f'Conexión establecida con {self.sv_address}:{self.sv_port}')

    def __getattr__(self, method):
        """Intercepta llamadas a métodos no definidos y las transforma en solicitudes XML."""
        def wrapper(*args):
            # TODO: Transformar método y parámetros a XML
            self.request_in_xml = None

            self.client_socket.send(self.request_in_xml.encode())
            print(f'Procedimiento enviado hacia el servidor {self.sv_address}:{self.sv_port}')
            
            print('Esperando respuesta...')
            self.response_in_xml = self.client_socket.recv().decode()
            # TODO: Transformar XML a resultados
            # Decidir si la conexión se cierra o se mantiene
        return wrapper

# =========================
# Clase Client
# =========================
class Client:
    client_socket = None
    my_address = None
    my_port = None

    def __init__(self):
        """Inicializa cliente con IP y puerto locales."""
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.my_address, self.my_port = self.client_socket.getsockname()
        print(f'Cliente creado con IP: {self.my_address} y puerto: {self.my_port}')

    def connect(self, address, port):
        """Crea una conexión hacia el servidor remoto."""
        return Connection(self.client_socket, address, port)

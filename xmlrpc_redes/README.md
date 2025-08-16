# 🖥️ Servidor y Cliente RPC con Sockets en Python

Este proyecto implementa un **servidor** y un **cliente** usando **sockets TCP**, simulando un sistema de **Remote Procedure Call (RPC)**.  
El cliente puede invocar métodos remotos en el servidor, enviando solicitudes en XML (aunque la serialización XML aún no está implementada en detalle).

---

## 📌 Código Principal

```python
import socket
import utils  # Módulo auxiliar para procesar XML (no incluido aquí)

# =========================
# Clase Server
# =========================
class Server:
    my_socket = None
    my_address = None
    my_port = None
    procedures = {}  # Diccionario de métodos disponibles

    def __init__(self, address, port):
        """Inicializa el servidor con dirección IP y puerto."""
        self.my_address = address
        self.my_port = port
        self.my_socket = socket(AF_INET, SOCK_STREAM)  # Crear socket TCP
        self.my_socket.bind((self.my_address, self.my_port))
        print(f'Servidor creado con IP: {self.my_address} y puerto: {self.my_port}')
    
    def add_method(self, method):
        """Agrega un procedimiento al diccionario de métodos."""
        if method in self.procedures:
            self.procedures[method.__name__] = method
            print('El procedimiento ya existía y ha sido actualizado.')
        else:
            self.procedures[method].__name__ = method
            print('El procedimiento ha sido agregado correctamente.')

    def serve(self):
        """Bucle principal para recibir y procesar solicitudes."""
        while True:
            print('El servidor está listo para recibir.')
            request_in_xml, cl_address_port = self.sv_socket.recvfrom()
            # TODO: Procesar XML
            # TODO: Ejecutar función con sus parámetros
            # TODO: Convertir resultados a XML
            response_in_xml = None
            self.my_socket.sendto(response_in_xml, cl_address_port)
            print('Resultado enviado hacia el cliente.')


# =========================
# Clase Connection
# =========================
class Connection:
    my_address = None
    my_port = None
    my_socket = None
    sv_address = None
    sv_port = None

    def __init__(self, address, port, sv_address, sv_port):
        """Inicializa la conexión con IP y puerto propios y del servidor."""
        self.my_address = address
        self.my_port = port
        self.sv_address = sv_address
        self.sv_port = sv_port
        self.my_socket = socket(AF_INET, SOCK_STREAM)  # Socket TCP del cliente

    def __call__(self, address, port, sv_address, sv_port):
        """Permite actualizar IP/puerto del cliente y del servidor."""
        self.my_address = address
        self.my_port = port
        self.sv_address = sv_address
        self.sv_port = sv_port

    def __getattr__(self, method):
        """Intercepta llamadas a métodos no definidos y las convierte en solicitudes XML."""
        def wrapper(*args):
            # TODO: Transformar método y parámetros a XML
            self.request_in_xml = None
            self.my_socket.sendto(self.request_in_xml, (self.sv_address, self.sv_port))
            print('Procedimiento enviado hacia el servidor.')
            print('Esperando respuesta...')
            response_in_xml, sv_address_port = self.my_socket.recvfrom()
            # TODO: Transformar XML a resultados
        return wrapper


# =========================
# Clase Client
# =========================
class Client:
    my_address = None
    my_port = None

    def __init__(self, address, port):
        """Inicializa cliente con dirección IP y puerto propios."""
        self.my_address = address
        self.my_port = port

    def connect(self, address, port):
        """Crea una conexión hacia un servidor remoto."""
        return Connection(self.my_address, self.my_port, address, port)

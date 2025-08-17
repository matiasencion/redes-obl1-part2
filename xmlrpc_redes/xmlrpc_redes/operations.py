import socket
import utils

class Server:
    server_welcoming_socket = None
    my_address = None
    my_port = None
    procedures = {}
    def __init__(self, address, port):
        self.server_welcoming_socket = socket(AF_INET, SOCK_STREAM)
        self.server_welcoming_socket.bind((address, port))
        self.my_address, self.my_port = self.server_welcoming_socket.getsockname()
        print('Servidor creado con IP: ' + self.my_address + ' y puerto: ' + self.my_port)
    
    def add_method(self, method):
        if method in self.procedures:
            self.procedures[method.__name__] = method
            print('El procedimiento ya existia previamente y ha sido actualizado.')
        else:
            self.procedures[method].__name__ = method
            print('El procedimiento ha sido agregado correctamente.')

    def serve(self):
        while True:
            self.server_welcoming_socket.listen(1) #SI EL SERVIDOR ESTA OCUPADO COMO MAXIMO PUEDE HABER UNA COLA DE 1 ESPERANDO
            print('El servidor esta listo para recibir.')
            connection_socket, cl_address_port = self.server_welcoming_socket.accept()
            print('Conexion establecida con ' + cl_address_port)
            request_in_xml = connection_socket.recv().decode()
            #PROCESAR XML
            #EJECUTAR FUNCION CON SUS PARAMETROS
            #PASAR A XML
            response_in_xml = None
            connection_socket.send(response_in_xml)
            print('Resultado enviado hacia el cliente ' + cl_address_port)
            connection_socket.close() # NO ES PERSISTENTE?

class Connection:
    client_socket = None
    sv_address = None
    sv_port = None
    request_in_xml = None
    response_in_xml = None
    def __init__(self, cl_socket, sv_address, sv_port):
        self.client_socket = cl_socket
        self.sv_address = sv_address
        self.sv_port = sv_port
        self.client_socket.connect((self.sv_address, self.sv_port))
        print('Conexion establecida con ' + self.sv_address + ':' + self.sv_port)

    def __getattr__(self, method):
        def wrapper(*args):
            #TRANSFORMAR FUNCION Y PARAMETROS A XML
            self.request_in_xml = None
        self.client_socket.send(self.request_in_xml.encode())
        print('Procedimiento enviado hacia el servidor ' + self.sv_address + ':' + self.sv_port)
        print('Esperando respuesta...')
        self.response_in_xml = self.client_socket.recv().decode()
        #TRANSFORMAR XML A RESULTADOS
        #HAY QUE VER SI SE CIERRA LA CONEXION O NO


class Client:
    client_socket = None
    my_address = None
    my_port = None
    def __init__(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.my_address, self.my_port = self.client_socket.getsockname()
        print('Cliente creado con IP: ' + self.my_address + ' y puerto: ' + self.my_port)

    def connect(self, address, port):
        return Connection(self.client_socket, address, port)
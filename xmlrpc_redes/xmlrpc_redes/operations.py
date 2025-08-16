import socket
import utils

class Server:
    my_socket = None
    my_address = None
    my_port = None
    procedures = {}
    def __init__(self, address, port):
        self.my_address = address
        self.my_port = port
        self.my_socket = socket(AF_INET, SOCK_STREAM)
        self.my_socket.bind((self.my_address, self.my_port))
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
            print('El servidor esta listo para recibir.')
            request_in_xml, cl_address_port = self.sv_socket.recvfrom()
            #PROCESAR XML
            #EJECUTAR FUNCION CON SUS PARAMETROS
            #PASAR A XML
            response_in_xml = None
            self.my_socket.sendto(response_in_xml, cl_address_port)
            print('Resultado enviado hacia el cliente.')

class Connection:
    my_address = None
    my_port = None
    my_socket = None
    sv_address = None
    sv_port = None
    def __init__(self, address, port, sv_address, sv_port):
        self.my_address = address
        self.my_port = port
        self.sv_address = sv_address
        self.sv_port = sv_port
        self.my_socket = socket(AF_INET, SOCK_STREAM)

    def __call__(self, address, port, sv_address, sv_port): #SI QUIERE CAMBIAR LA DIRECCION IP O PUERTO DEL SERVIDOR y SU PROPIA IP O PUERTO
        self.my_address = address
        self.my_port = port
        self.sv_address = sv_address
        self.sv_port = sv_port

    def __getattr__(self, method):
        def wrapper(*args):
            None
            self.request_in_xml = None
            #TRANSFORMAR FUNCION Y PARAMETROS A XML
        self.my_socket.sendto(self.request_in_xml, (self.sv_address, self.sv_port))
        print('Procedimiento enviado hacia el servidor.')
        print('Esperando respuesta...')
        response_in_xml, sv_address_port = self.my_socket.recvfrom()
        #TRANSFORMAR XML A RESULTADOS


class Client:
    my_address = None
    my_port = None
    def __init__(self, address, port):
        self.my_address = address
        self.my_port = port

    def connect(self, address, port):
        return Connection(self.my_address, self.my_port, address, port)
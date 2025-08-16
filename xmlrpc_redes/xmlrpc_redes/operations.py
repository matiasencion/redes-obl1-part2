from socket import *

class Server:
    sv_socket = None
    my_address = None
    my_port = None
    request = None
    cl_address_port = None
    procedures = {}
    def __init__(self, address, port):
        self.my_address = address
        self.my_port = port
        self.sv_socket = socket(AF_INET, SOCK_STREAM)
        self.sv_socket.bind((self.my_address, self.my_port))
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
            request, cl_address_port = self.sv_socket.recvfrom()
            #FUNCIONALIDAD DEL SERVIDOR
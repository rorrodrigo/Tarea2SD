from concurrent import futures
import grpc
import time
import msn_pb2
import msn_pb2_grpc
import threading


class ServerMSN(msn_pb2_grpc.ServidorMSNServicer):
    def __init__(self):
        self.puertoactual = 5010
        self.clientes = []
        self.mensajes = {}
        self.semaforo = threading.Semaphore(1)

    def DevolverUsuarios(self, request_iterator, context):
        usuarios = []
        lista_usuarios = msn_pb2.Usuario()

        if(len(self.clientes) == 0):
            lista_usuarios.username = ""
            return lista_usuarios
        else:
            for username in self.clientes:    
                usuarios.append(username)
        
        lista_usuarios.username = ', '.join(usuarios)                
        return lista_usuarios
    
    def ValidarUsuario(self, request_iterator, context):
        ack = msn_pb2.Ack()
        if(request_iterator.username in self.clientes):
            ack.ack = "nack"
        else:
            (self.clientes).append(request_iterator.username)
            (self.mensajes)[request_iterator.username] = []
            ack.ack = "ack"
        return ack
    
    def RecibirMensaje(self,request,context):
        rsp = msn_pb2.Mensaje()
        if(request.username in self.mensajes):
            for mensaje in self.mensajes[request.username]:
                yield mensaje

    def EnviarMensaje(self,req,context):
        emisor = req.emisor
        receptor = req.receptor
        mensaje = req.mensaje
        marcatemp = req.marcatiempo
        if(receptor in self.mensajes):
            self.mensajes[receptor].append(req)
        else:
            self.mensajes[receptor]=[]
            self.mensajes[receptor].append(req)
        if(marcatemp == ""):
            confirmation = msn_pb2.Ack()
            confirmation.ack = "ack"
            return confirmation
        self.semaforo.acquire()
        log = open("log.txt", "a")
        log.write(emisor + "@" + receptor + "@" + mensaje + "@" + marcatemp + "\n")
        log.close()
        self.semaforo.release()
        confirmation = msn_pb2.Ack()
        confirmation.ack = "ack"
        return confirmation

    def DevolverMensajes(self,request,context):
        self.semaforo.acquire()
        log = open("log.txt", "r")
        for mensaje in log:
            #emisor @ receptor @ msj @ marcatemp
            m = mensaje.strip().split("@")
            if(m[0] == request.username):
                msj = msn_pb2.Mensaje()
                msj.emisor = m[0]
                msj.receptor = m[1]
                msj.mensaje = m[2]
                msj.marcatiempo = m[3]
                yield msj
        log.close()
        self.semaforo.release()
        return

    def Desconectarse(self,request,context):
        confirmacion = msn_pb2.Ack()
        if(request.username in self.clientes):
            self.clientes.remove(request.username)
            confirmacion.ack = "ack"
        return confirmacion


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor())
    msn_pb2_grpc.add_ServidorMSNServicer_to_server(ServerMSN(), server)
    address = 'localhost'
    port = 5010
    server.add_insecure_port(address + ":" + str(port))
    server.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        server.stop(0)
        



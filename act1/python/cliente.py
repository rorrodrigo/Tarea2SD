from concurrent import futures
import grpc
import sys
import msn_pb2
import msn_pb2_grpc
import threading
from datetime import datetime

class Cliente():
    def __init__(self):
        self.clientes = set([])
        self.leidos = []
        self.emisor = ""
        self.receptor = ""
        self.mensaje = ""
        self.semaforo = threading.Semaphore(1)
        self.chat_flag = False

        direccion = "localhost"
        puerto = 5010

        canal = grpc.insecure_channel(direccion+":"+str(puerto))
        self.conn = msn_pb2_grpc.ServidorMSNStub(canal)
        
        usuario = msn_pb2.Usuario()
        while True:
            id = input("Ingrese un nombre de usuario unico: ")
            usuario.username = id
            self.cliente = usuario
            respuesta = self.conn.ValidarUsuario(usuario)
            if(respuesta.ack == "nack"):
                print("Ese nombre de usuario se encuentra ocupado:\n")
                ids_usados = self.conn.DevolverUsuarios(usuario)
                print(ids_usados)
                ids_usados = (ids_usados.username).split(", ")
                self.clientes = set(ids_usados)
            else:
                self.emisor = id
                self.id = id
                break

        self.menu()

    def EnviarMensaje(self):
        respuesta = msn_pb2.Ack()
        msj = msn_pb2.Mensaje()
        msj = self.Input_Usuario()
        if((msj.receptor == "user") and (msj.mensaje == "0")):
            self.chat_flag = False
            return
        respuesta = self.conn.EnviarMensaje(msj)
        if(respuesta.ack == "ack"):
            return
        else:
            self.chat_flag = False
            print("Hubo un error en la entrega del mensaje: "+mensaje.receptor+"@"+mensaje.mensaje)
            return

    def Input_Usuario(self):
        while True:
            mensaje = input()
            if(mensaje == ""):
                msj = msn_pb2.Mensaje()
                msj.mensaje = "nack"
                return msj
            elif(mensaje == "0"):
                msj = msn_pb2.Mensaje()
                msj.receptor = "user"
                msj.mensaje = "0"
                return msj
            m = mensaje.strip().split("@")
            msj = msn_pb2.Mensaje()
            msj.emisor = self.emisor
            msj.receptor = m[0]
            msj.mensaje = m[1]
            now = datetime.now()
            taim = now.strftime('%d/%m/%Y %H:%M:%S')
            msj.marcatiempo= taim
            return msj

    def RecibirMensajes(self):
        text = msn_pb2.Mensaje()
        for text in self.conn.RecibirMensaje(self.cliente):
            if(text in self.leidos):
                continue
            else:
                self.leidos.append(text)
                print("|{}|[{}] >> {}".format(text.marcatiempo,text.emisor,text.mensaje))
        return

    def Historial(self):
        print("Historial de mensajes:\n")
        for msj in self.conn.DevolverMensajes(self.cliente):
            print(msj)
        print("_____________________________________________________________________")
        return

    def UsuariosConectados(self):
        conectados = self.conn.DevolverUsuarios(self.cliente)
        conectados = set(conectados.username.split(", "))
        if((len(self.clientes) == 0) and (len(conectados)==0)):
            print("")
        elif(self.clientes != conectados):
            members = ""
            if(len(conectados)<len(self.clientes)):
                idos = self.clientes - conectados
                print("Se ha(n) ido del chat: ")
                for user in idos:
                    members = members + user + ", "
                print(members + "\n")
                self.clientes = conectados
            elif(len(conectados)>len(self.clientes)):
                nuevos = conectados - self.clientes 
                print("Se ha(n) unido al chat: ")
                for user in nuevos:
                    members = members + user + ", "
                print(members + "\n")
                self.clientes = conectados
            else:
                idos = self.clientes - conectados
                nuevos = conectados - self.clientes
                print("Se ha(n) ido al chat: ")
                for user in idos:
                    members = members + user + ", "
                print(members + "\n")
                print("Se ha(n) ido del chat: ")
                members = ""
                for user in nuevos:
                    members = members + user + ", "
                print(members + "\n")
                self.clientes = conectados
        print("Usuarios activos: ")
        members = ""
        for user in self.clientes:
            members = members + user + ", "
        print(members)
        print("_____________________________________________________________________")
        return

    def Desconectar(self):
        rsp = self.conn.Desconectarse(self.cliente)
        if(rsp.ack == "ack"):
            print("Conexion finalizada.")
            return
        else:
            print("No se ha podido desconectar.\n")
            return

    def menu(self):
        while True:
            print("Seleccione una opcion:\n1)Chatear.\n2)Obtener los clientes activos.\n3)Obtener mensajes enviados.\n(0 para salir)")
            opcion = input()
            if(opcion == ""):
                continue
            else:
                opcion = int(opcion)
            if(opcion == 1):
                print("_____________________________________________________________________________")
                print("Para enviar un mensaje a alguien debe escribir usuario@mensaje, '0' para salir")
                print("_____________________________________________________________________________")
                self.chat_flag = True
                self.UsuariosConectados()
                while(self.chat_flag):
                    threading.Thread(target=self.RecibirMensajes(), daemon=True, args={}).start()
                    threading.Thread(target=self.EnviarMensaje(), daemon=True, args={}).start()
            elif(opcion == 2):
                self.UsuariosConectados()
            elif(opcion == 3):
                self.Historial()
            elif(opcion == 0):
                print("Cerrando conexion...")
                self.Desconectar()
                sys.exit()
            else:
                print("Opcion invalida.\n")
        

if __name__ == '__main__':
    cliente = Cliente()
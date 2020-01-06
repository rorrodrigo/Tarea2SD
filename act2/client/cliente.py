import threading
import sys
import pika
import uuid
import json
import time
from datetime import datetime

class Cliente:
    def __init__(self):
        self.connectStatus = False
        self.key_route = str(uuid.uuid4())
        self.nombre = ""
        while(not(self.connectStatus)):
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit_server'))
                self.connectStatus = True
            except pika.exceptions.AMQPConnectionError:
                self.connect = False
                print ("Conectando al Servidor...")
                time.sleep(4)

        self.LoginCH = self.connection.channel()
        self.LoginCH.exchange_declare(exchange='Login', exchange_type='direct')
        self.ChatCH = self.connection.channel()
        self.ChatCH.exchange_declare(exchange='Chat', exchange_type='direct')
        self.viewCH = self.connection.channel()
        self.viewCH.exchange_declare(exchange='View', exchange_type='direct')
        self.Login()
        threading.Thread(target=self.Receive, daemon=True).start()
        self.doSomething()

    def Login(self):
        result = self.LoginCH.queue_declare(queue='', exclusive=True)
        queue = result.method.queue
        mensaje = {"key_route":self.key_route}
        Flag = True
        while Flag:
            self.nombre = str(input("Ingrese Nombre de Usuario: "))
            mensaje["nombre"] = self.nombre
            self.LoginCH.queue_bind(exchange='Login', queue = queue, routing_key = self.key_route)
            self.LoginCH.basic_publish(exchange='Login', routing_key='Login', body=json.dumps(mensaje))
            _,_,recibido = next(self.LoginCH.consume(queue))

            if recibido.decode() == "OK":
                Flag = False


        self.viewQueue = self.viewCH.queue_declare(queue='', exclusive=True).method.queue
        self.viewCH.queue_bind(exchange = "View", queue = self.viewQueue, routing_key = self.key_route)

    def ReceiveCallBack(self, ch, method, properties, body):
        recibido = json.loads(body)
        mostrar = recibido['date']+" |  "+recibido['origen']+" te ha enviado un mensaje: "+recibido["msg"]+"\n"
        print ("\n"+ mostrar)

    def Receive(self):
        nueva = pika.BlockingConnection(pika.ConnectionParameters('rabbit_server'))
        chat = nueva.channel()
        inBoxQ = chat.queue_declare(queue='', exclusive=True).method.queue
        chat.exchange_declare(exchange='Chat', exchange_type='direct')
        chat.queue_bind(exchange='Chat', queue = inBoxQ, routing_key = self.key_route)
        chat.basic_consume(queue = inBoxQ, on_message_callback = self.ReceiveCallBack, auto_ack=True)
        chat.start_consuming()

    def crearMensaje(self,origenName,destinoName,msg,accion):
        dateStamp = datetime.now()
        data = {
        "date": dateStamp.strftime("%D %H:%M:%S"),
        "destino": destinoName,
        "msg": msg,
        "origen": origenName,
        "accion":accion
        }
        return data

    def doSomething(self):
        Flag = True
        while Flag:
            print ("\n____________________________________________________\nAcciones disponible\n")
            print("\t1 - Ver lista de usuarios conectados.")
            print("\t2 - Ver Historial de mensajes enviados")
            print("\t3 - Enviar mensaje")
            accion = str(input("\nIntroduzca el numero de la accion que desea realizar: "))

            if accion == "1":
                mensaje = self.crearMensaje(self.nombre,"","","View_Users")
                self.viewCH.basic_publish(exchange='View', routing_key="View", body=json.dumps(mensaje))
                _,_,recibido = next(self.viewCH.consume(self.viewQueue))
                print ("\nUsuarios Activos en el Chat: ")
                print (recibido.decode())

            elif accion == "2":
                mensaje = self.crearMensaje(self.nombre,"","","View_Msg")
                self.viewCH.basic_publish(exchange='View', routing_key="View", body=json.dumps(mensaje))
                _,_,recibido = next(self.viewCH.consume(self.viewQueue))
                recibido = json.loads(recibido)
                print("Mensajes enviados :\n")
                for m in recibido['mensajes']:
                    print (m)

            elif accion == "3":
                print ("Ingrese Mensaje y Destinatario\n")
                dest = str(input("Destinatario: "))
                msj = str(input("Mensaje: "))
                mensaje = self.crearMensaje(self.nombre,dest,msj,"Send_Msg")
                self.ChatCH.basic_publish(exchange='Chat', routing_key="Chat", body=json.dumps(mensaje))

cliente = Cliente()

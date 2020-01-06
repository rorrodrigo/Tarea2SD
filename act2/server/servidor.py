import threading
import sys
import pika
import uuid
import json
import time

class Server:
    def __init__(self):
        self.connectStatus = False
        self.users = {}
        self.idMsg = 0
        self.mutex = threading.Lock()
        log = open("log.txt", "w")
        log.close()
        while(not(self.connectStatus)):
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit_server'))
                self.connectStatus = True
            except pika.exceptions.AMQPConnectionError:
                self.connect = False
                print ("Iniciando Servidor...")
                time.sleep(4)

        Views = threading.Thread(target=self.Views_thread, daemon=True).start()
        Chat = threading.Thread(target=self.Chat_thread, daemon=True).start()

        self.LoginCH = self.connection.channel()
        self.LoginCH.exchange_declare(exchange='Login', exchange_type='direct')
        self.QLogin = self.LoginCH.queue_declare(queue='', exclusive=True).method.queue
        self.LoginCH.queue_bind(exchange= "Login", queue= self.QLogin, routing_key = "Login")
        self.LoginCH.basic_consume(queue=self.QLogin, on_message_callback=self.LoginCallback, auto_ack=True)
        self.LoginCH.start_consuming()

    def LoginCallback(self, ch, method, properties, body):
        recibido = json.loads(body)
        nombre = recibido["nombre"]
        key = recibido["key_route"]

        if nombre not in self.users.keys():
            self.users[nombre]= key
            self.LoginCH.basic_publish(exchange='Login', routing_key = key, body = "OK".encode())
        else:
            self.LoginCH.basic_publish(exchange='Login', routing_key = key, body = "USADO".encode())

    def Views_thread(self):
        self.View = pika.BlockingConnection(pika.ConnectionParameters('rabbit_server'))
        self.ViewCH = self.View.channel()
        self.ViewCH.exchange_declare(exchange='View', exchange_type='direct')
        self.viewQueue = self.ViewCH.queue_declare(queue='', exclusive=True).method.queue
        self.ViewCH.queue_bind(exchange= "View", queue= self.viewQueue, routing_key = "View")
        self.ViewCH.basic_consume(queue=self.viewQueue, on_message_callback=self.ViewsCallback, auto_ack=True)
        self.ViewCH.start_consuming()

    def ViewsCallback(self, ch, method, properties, body):
        recibido = json.loads(body)
        user_name = recibido["origen"]
        accion = recibido["accion"]

        if accion == "View_Users":
            mensaje = ""
            for user in self.users.keys():
                mensaje = mensaje + user + "/"
            self.ViewCH.basic_publish(exchange='View', routing_key = self.users[user_name], body = mensaje.encode())
        elif accion == "View_Msg":
            mensajes = []
            self.mutex.acquire()
            log = open("log.txt", "r")
            for linea in log:
                #id@ emisor @ receptor @ msj @ marcatemp
                m = linea .strip().split("@")
                if(m[1] == user_name):
                    string = m[4] + "  |  " + "Mensaje enviado a "+ m[2]+" : "+ m[3]
                    mensajes.append(string)
            if len(mensajes)==0:
                mensajes.append("No ha enviado mensajes")
            log.close()
            self.mutex.release()
            data = {"mensajes": mensajes}
            self.ViewCH.basic_publish(exchange='View', routing_key = self.users[user_name], body = json.dumps(data))

    def Chat_thread(self):
        self.Chat = pika.BlockingConnection(pika.ConnectionParameters('rabbit_server'))
        self.ChatCH = self.Chat.channel()
        self.ChatCH.exchange_declare(exchange='Chat', exchange_type='direct')
        self.ChatQueue = self.ChatCH.queue_declare(queue='', exclusive=True).method.queue
        self.ChatCH.queue_bind(exchange= "Chat", queue= self.ChatQueue, routing_key = "Chat")
        self.ChatCH.basic_consume(queue=self.ChatQueue, on_message_callback=self.ChatCallback, auto_ack=True)
        self.ChatCH.start_consuming()

    def ChatCallback(self, ch, method, properties, body):
        recibido =  json.loads(body)
        user_name = recibido["origen"]
        dest_name = recibido["destino"]
        date = recibido["date"]
        msj = recibido["msg"]

        if dest_name in self.users.keys():
            self.ChatCH.basic_publish(exchange = "Chat", routing_key = self.users[dest_name], body = json.dumps(recibido))

        self.mutex.acquire()
        log = open("log.txt", "a+")
        linea = str(self.idMsg)+"@"+user_name+"@"+dest_name+"@"+msj+"@"+date+"\n"
        log.write(linea)
        log.close()
        self.idMsg+=1
        self.mutex.release()

server = Server()

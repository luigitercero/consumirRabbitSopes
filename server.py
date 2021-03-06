#!/usr/bin/env python
import pika
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement



credentials = pika.PlainCredentials('admin', '123')
parameters = pika.ConnectionParameters('35.229.58.120',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='colaCassandra')

def actualizarUser(datos):
    pass
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    listaAc = datos.split(',')
#    print(int(listaAc[0]))
#    print("%d"%(int(listaAc[0])))
    session.execute(SimpleStatement("UPDATE bduser.usuario2 SET contra = %s , nombre = %s, apellido = %s, fecha = %s WHERE nombre_usuario = %s"), (listaAc[1],listaAc[2],listaAc[3],listaAc[4],listaAc[0],));      
    return "se actualizo"

def insertarBd(datos):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    listaDt = datos.split(',')
    
    print(listaDt[0])
    print(listaDt[1])
    print(listaDt[2])
    print(listaDt[3])
    print(listaDt[4])
    prepared = session.prepare("""
    INSERT INTO bduser.usuario2 ( nombre_usuario, contra, nombre, apellido, fecha)
    VALUES ( ?, ?, ?, ?, ?)
        """)
    session.execute(prepared.bind((listaDt[0], listaDt[1], listaDt[2], listaDt[3], listaDt[4])))
    return 3
def accederUser(datos):
    pass
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    listaDatos = datos.split(',')
    rows = session.execute("SELECT * FROM bduser.usuario2")
    for row in rows:
#        print row[0], row[1], row[2]
	name = row.nombre_usuario
	name2 = name.encode("utf-8")
	passa = row.contra
	passa2 = passa.encode("utf-8")
        if name == listaDatos[0]:
            pass
	    if	passa == listaDatos[1]:
            	pass
		return 1
	    return '-1'
    return '-2'
  
def accion(body):
    cuerpo = str(body).split('#%')
    print(cuerpo[0])	
    if cuerpo[0]=='nuevo':
        pass
        return insertarBd(cuerpo[1])
    else:
        if cuerpo[0]=='login':
            return accederUser(cuerpo[1])
        else:
            if cuerpo[0]=='getdatos':
                return veruser(cuerpo[1])
            else:
                if cuerpo[0]=='update':
                    return actualizarUser(cuerpo[1])
 
def veruser(datos):
    pass
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    listaDatos = datos.split(',')
    print(listaDatos[0]+"esto envio el Kevin")
    rows = session.execute("SELECT * FROM bduser.usuario2")
    for row in rows:
#        print row[0], row[1], row[2]
	name = row.nombre_usuario
	name2 = name.encode("utf-8")
	passa = row.contra
	passa2 = passa.encode("utf-8")
        if name == listaDatos[0]:
            pass
	    return row.nombre+","+row.apellido+","+row.contra
	   
    return '-2'
   
 
def mostrar():
    pass
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    rows = session.execute("SELECT * FROM bduser.usuario2")
    datosMostrar = ""
    for row in rows:
        datosMostrar = datosMostrar  +","+row.nombre_usuario.encode("utf-8") + "," + row.contra.encode("utf-8") + "," + row.nombre.encode("utf-8") + "," + row.apellido.encode("utf-8") +  "," + row.fecha.encode("utf-8") + " | "
    return datosMostrar

def on_request(ch, method, props, body):
    #n = int(body)

    print(" [.] usuarios: %s " % body)

    val = str(body)
    response = accion(val)
    print (response)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='colaCassandra')

print(" [x] Awaiting RPC requests")
channel.start_consuming()


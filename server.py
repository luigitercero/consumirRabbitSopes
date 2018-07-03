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

def insertarBd(datos):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    listaDt = datos.split(',')
    prepared = session.prepare("""
    INSERT INTO bduser.usuario ( nombre_usuario, contra, nombre, apellido, fecha)
    VALUES ( ?, ?, ?, ?, ?)
        """)
    session.execute(prepared.bind( listaDt[0], listaDt[1], listaDt[2], listaDt[3], listaDt[4]))
    return 'nuevoUsuario'
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
		return str(row.id_usuario)
	    return '-1'
    return '-1'
  
def accion(body):
    cuerpo = str(body).split('#%')
    print(cuerpo[0])	
    if cuerpo[0]=='crear':
        pass
        return insertarBd(cuerpo[1])
    else:
        return accederUser(cuerpo[1])


def on_request(ch, method, props, body):
    #n = int(body)

    print(" [.] usuarios: %s " % body)

    val = str(body)
    response = accion(val)

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


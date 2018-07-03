#!/usr/bin/env python
import pika
import redis
credentials = pika.PlainCredentials('admin', '123')
parameters = pika.ConnectionParameters('35.229.58.120',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='mensaje')


def guardarDatos(mensaje):
    redis_entidades = redis.Redis(
        host='35.239.110.78',
        port=6379,
        password='fVj1HjMcLYXE',
        db=1)
    redis_entidades.rpush('comentario3', mensaje)
    return 1

def retornar():
    redis_entidades = redis.Redis(
        host='35.239.110.78',
        port=6379,
        password='fVj1HjMcLYXE',
        db=1)
    a=redis_entidades.lrange("comentario3", 0, -1)
    return a;



def on_request(ch, method, props, body):
    spl = str(body).split('$')
    print(spl[0])
    if (spl[0]=='b\'nuevo'):
    
        response = guardarDatos(spl[1])
        print(response)
    else:
        response = retornar()
        print(response)  
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='mensaje')

print(" [x] Awaiting RPC requests")
channel.start_consuming() 

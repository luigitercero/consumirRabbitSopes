#!/usr/bin/env python
import pika


credentials = pika.PlainCredentials('admin', '123')
parameters = pika.ConnectionParameters('35.229.58.120',
                                       5672,
                                       '/',
                                       credentials)


channel = connection.channel()


channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()

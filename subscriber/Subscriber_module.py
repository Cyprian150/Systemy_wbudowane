import paho.mqtt.client as paho
import os

def on_message(mosq, obj, msg):
    print ("%-20s %d %s" % (msg.topic, msg.qos, msg.payload))
    mosq.publish('pong', 'ack', 0)

def on_publish(mosq, obj, mid):
    pass

if __name__ == '__main__':

    mqtt_host_name = os.getenv("mqtt_host_name", "localhost")
    mqtt_topic = os.getenv("mqtt_topic", "AirQuality")

    client = paho.Client()
    client.on_message = on_message
    client.on_publish = on_publish

    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    client.connect(mqtt_host_name, 1883, 60)

    client.subscribe(mqtt_topic, 0)

    while client.loop() == 0:
        pass

# vi: set fileencoding=utf-8 :
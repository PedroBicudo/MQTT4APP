import paho.mqtt.client as mqtt
import connectors as cn
from mosquitto_config import \
    mqtt_ID, \
    mqtt_server, \
    mqtt_port, \
    mqtt_user, \
    mqtt_passwd, \
    mqtt_qos


def on_connect(client, userdata, flags, rc):
    print("Connected :)")
    client.subscribe("/home/horta/#", mqtt_qos)  # Topicos + Qos


def on_message(client, userdata, msg):
    _id = str(msg.topic[12:17])
    topico = str(msg.topic[18:])
    valor = int(msg.payload)

    print(topico)
    cn.connect_back4app(_id, topico, valor)


client = mqtt.Client( "%s" % mqtt_ID )
client.on_connect = on_connect
client.on_message = on_message

if mqtt_user and mqtt_passwd:
    client.username_pw_set( mqtt_user, password="%s" %mqtt_passwd)
    client.connect("%s" % mqtt_server, int(mqtt_port), 60)
    client.loop_forever()
else:
    print("Usuário ou senha não informados")
    print("Falha na conexao")





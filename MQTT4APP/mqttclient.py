from paho.mqtt.client import *
from connectors import *
from mosquitto_config import *

def on_connect(client, userdata, flags, rc):
    print("Connected :)")
    client.subscribe("/home/horta/#", mqtt_qos)  # Topicos + Qos


def on_message(client, userdata, msg):
    steps = Msteps( str(msg.topic), int(msg.payload), back_app_id, back_rest_id)
    steps.filtro_id()
    steps.sensor()
    steps.connect_back4app()


client = Client( "%s" % mqtt_ID )
client.on_connect = on_connect
client.on_message = on_message

if mqtt_user and mqtt_passwd:
    client.username_pw_set( mqtt_user, password="%s" %mqtt_passwd)
    client.connect("%s" % mqtt_server, int(mqtt_port), 60)
    client.loop_forever()
else:
   print("Usuário ou senha não informados")
   print("Falha na conexao")





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
    topico_mqtt = str(msg.topic)
    valor = int(msg.payload)

    # Variaveis filtro
    topic_b, topic_e = 0, 12
    id_b, id_e = 0, 3

    # Topic ID
    while True:
        topic_b += 1
        topic_e += 1
        if topico_mqtt[topic_b:topic_e - 1:] == "temperatura":
            topic_e -= 1
            break
        elif topico_mqtt[topic_b:topic_e:] == "luminosidade":
            break
        else:
            if topico_mqtt[topic_b:topic_e - 5:] == "umidade":
                topic_e -= 5
                break
            if topic_b > len(topico_mqtt) or topic_b > len(topico_mqtt):
                #print("NÃo encontrado")
                break

    # Sensor ID
    while True:
        id_b += 1
        id_e += 1
        if topico_mqtt[id_b:id_e:] == "id_":
            id_b += 3
            id_e += 5
            break
        if id_b > len(topico_mqtt) or id_b > len(topico_mqtt):
            #print("NÃo encontrado")
            break

    # Define sensor e identificação
    sensor = topico_mqtt[topic_b:topic_e:]
    _id = topico_mqtt[id_b:id_e:]

    # Verificar se variavel existe
    if sensor and _id:
        print("""
        Topico: %s
        ID: %s 
        Valor: %d\n\n
        Resultado:""" %( sensor, _id, valor)
              )
    else:
        print("Erro, algum valor não foi definido corretamente")
        exit(1)

    # Conectar
    cn.connect_back4app(_id, sensor, valor)


client = mqtt.Client( "%s" % mqtt_ID )
client.on_connect = on_connect
client.on_message = on_message

if mqtt_user and mqtt_passwd:
    client.username_pw_set( mqtt_user, password="%s" %mqtt_passwd)
    client.connect("%s" % mqtt_server, int(mqtt_port), 60)
    client.loop_forever()
else:
    print("Usuário ou senha não informados.")
    print("Falha na conexao.")





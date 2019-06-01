"""Script responsavel por simular um sensor."""
import paho.mqtt.publish as mqtt
import random as rd
import time as tm
import sys


def makeRandomData(topic, mqtt_ID):
    """Gerar valores aleatorios em tres topicos.

    topic: Topico a ser acessado
    mqtt_ID: Identificacao da conexao

    Tipo de retorno: List
    """
    valores = rd.sample(range(0, 100), 4)
    patt_topic = "{}{}".format(topic, mqtt_ID)
    msgs = [
            {
                'topic': '{}/temperatura'.format(patt_topic),
                'payload': '{}'.format(valores[1])
            },
            {
                'topic': '{}/umidade'.format(patt_topic),
                'payload': '{}'.format(valores[2])
            },
            {
                'topic': '{}/luminosidade'.format(patt_topic),
                'payload': '{}'.format(valores[3])
            }
           ]

    return msgs


def makePublish(sleep, mqtt_ID, host, auth, port, **kwargs):
    """Loop para realizar as publicacoes de valores aleatorios.

    sleep: Intervalo entre mensagens
    mqtt_ID: Identificacao da conexao
    host: Endereco do Broker
    port: Porta de acesso usado pelo Broker

    Tipo de retorno: None
    """
    print('='*100)
    while True:
        msgs = makeRandomData(mqtt_ID=mqtt_ID, **kwargs)
        # PUBLISH + AUTH
        mqtt.multiple(
                        msgs,
                        hostname=host,
                        port=port,
                        client_id=mqtt_ID,
                        auth=auth
                    )
        print('\n'.join(str(topic) for topic in msgs))
        print('='*100)
        tm.sleep(sleep)


def main(topic='/home/horta/',
         mqtt_ID='teste',
         sleep=10.0,
         host='127.0.0.1',
         port=1883,
         user='mygarden',
         password='123'
         ):
    """Conectar ao Broker e enviar valores aleatorios em topicos.

    topic: Topico a ser usado
            Estrutura:
                /caminho/do/topico/

    mqtt_ID: Identificacao da conexao
    sleep: Intervalo entre mensagens
    host: Endereco do Broker
    port: Porta de acesso usado pelo Broker
    user: Usuario para autenticacao
    password: Senha para autenticacao

    Tipo de retorno: None
    """
    assert float(sleep), 'O formato de time deve ser int ou float.'
    assert port.isnumeric(), 'O formato de time deve ser int.'
    auth = {'username': user, 'password': password}

    makePublish(
                sleep=float(sleep),
                mqtt_ID=mqtt_ID,
                host=host,
                auth=auth,
                port=int(port),
                topic=topic
                )


if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        main(*args)
    except Exception as err:
        print("""
    Como usar?
    mqttpublish.py  [topic] [mqtt_ID] [sleep] [host] [port] [user] [password]
              """)

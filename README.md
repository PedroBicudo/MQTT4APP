# Trabalho de conclusão de curso
#### Python (3.7.2)

## Instalação do módulo essencial para o projeto
Windows
```
pip install -r requirements.txt
```

## Testes unitários no projeto
Windows
```
python -m unittest discover tests
```

## Apresentação da interface de linha de comando
```
$ python tcc.py --help
usage: tcc.py [-h] -server MQTT_SERVER -topics [TOPICS [TOPICS ...]]
              [-backid BACKID] [-backrest BACKREST] [-backdb BACKDB]
              [-port MQTT_PORT] [-clientid CLIENTID] [-user USER]
              [-passw PASSW] [-qos QOS] [-transport TRANSPORT]

Projeto TCC SENAI DE REDES

optional arguments:
  -h, --help            show this help message and exit

Parametro Obrigatorio:
  -server MQTT_SERVER   Endereço de IP do Servidor MQTT.
  -topics [TOPICS [TOPICS ...]], -T [TOPICS [TOPICS ...]]
                        Topico(s) a ser(em) monitorado(s).
  -backid BACKID, -Bi BACKID
                        Back4app ID
  -backrest BACKREST, -Br BACKREST
                        Back4app REST
  -backdb BACKDB, -Bdb BACKDB
                        Nome do banco de dados Back4app.

Parametros nao obrigatorios:
  -port MQTT_PORT       Porta utilizada pelo servidor MQTT.
  -clientid CLIENTID    Identificacao da conexao.
  -user USER, -U USER   Usuario para acesso.
  -passw PASSW, -P PASSW
                        Senha de acesso.
  -qos QOS, -Q QOS      Nivel de qualidade de servico.
  -transport TRANSPORT, -Tr TRANSPORT
                        Protocolo de transporte
```


## Exemplos de uso
Exemplo de conexão com o módulo mqtt4app.py
```
>>> from mqtt4app import Mqtt4App
>>> project = Mqtt4App(topics=['a', 'b', 'c'])
>>> project.start_connection('192.168.0.10', 1883)
```

Exemplo de conexão via linha de comando
```
$ python tcc.py -server 192.168.0.10 -port 1883 -T a b c
```

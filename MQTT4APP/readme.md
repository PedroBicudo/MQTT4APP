# MQTT4APP
# Introdução:
<p>O arquivo mqtt4app.py tem a funcao de conectar, monitorar e enviar dados referentes as configuracoes realizadas manualmente ou no arquivo INI.</p>

# Requisito:
+ Python 3.

# Como usar?
## Metodo 1 - Via Import:

#### Etapas de importação
```
# Importando a classe 
from mqtt4app import Mqtt4App

# Instancia 
mqtt4app = Mqtt4App(
                        broker_address, port, qos,
                        topic_path, client_id, back_app_id,
                        back_rest_id, back_dbname, sensors, micr_ids
                        )

# Efetuar a conexao
mqtt4app.connectToBroker(auth={'username': username, 'password': passwd})

# Mostrar informacoes referentes ao servidor Broker( ip, porta, topico, qos )
print(mqtt4app)
```
#### Exemplo de criação de instância:
```
mqtt4app = Mqtt4App(
                        "127.0.0.1", 1883, 0,
                        "/home/horta/", "teste", 123123,
                        123123, "sensores", 
                        ["umidade", "luminosidade", "temperatura"], 
                        ["nodeA", "nodeB", "nodeC"]
                    )
```

#### Exemplo com Autenticação:
```
mqtt4app.connectToBroker(auth={'username': 'mygarden', 'password': '123'})
```
#### Exemplo sem Autenticação:
```
mqtt4app.connectToBroker()
```

## Metodo 2 - Via arquivo .INI:
<p>Esse metodo é dividido em duas etapas ( configuração de arquivo e execução main.py).</p>

### Etapa 1 - Configuração do arquivo .INI:

mosquitto_config.ini
```
[SERVER_SETTINGS]
mqtt_server = Endereço do servidor Broker
mqtt_port = Porta utilizada pelo servidor Broker
mqtt_ID = Identificacao da conexao a ser realizada
mqtt_qos = Nivel de qualidade de serviço
mqtt_topic = /caminho/para/o/sensor

# Caso não seja necessária, deixar os campos de autenticação em branco.
mqtt_user = usuario de autenticacao
mqtt_passwd = senha de autenticacao

[SENSORS_SETTINGS]
sensors = Nome dos sensores disponiveis
micr_ids = Nome dos microcontroladores disponiveis

[BACK4APP]
back_app_id = APP_ID
back_rest_id = REST_ID
back_dbname = Nome do banco de dados criado
```

#### Exemplo com Autenticação:
mosquitto_config.ini
```
[SERVER_SETTINGS]
mqtt_server = 127.0.0.1
mqtt_port = 1883
mqtt_ID = TCCREDES
mqtt_user = mygarden
mqtt_passwd = 123
mqtt_qos = 0
mqtt_topic = /home/horta/

[SENSORS_SETTINGS]
sensors = umidade, temperatura, luminosidade
micr_ids = node_hortaNorte, node_hortaLeste, node_hortaSul, node_hortaOeste

[BACK4APP]
back_app_id = [omitido] :)
back_rest_id = [omitido] :)
back_dbname = sensores
```

#### Exemplo sem Autenticação:
mosquitto_config.ini
```
[SERVER_SETTINGS]
[...]
mqtt_user = 
mqtt_passwd = 
[...]
```

### Etapa 2 - Execução do arquivo Main:
```
python main.py
```


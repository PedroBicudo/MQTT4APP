# MQTT4APP
## Introdução:
<p>O arquivo mqtt4app.py tem a funcao de conectar, monitorar e enviar dados referentes as configuracoes realizadas manualmente ou no arquivo INI.</p>

# Como usar?
## Metodo 1 - Via linha de comando:
```
python [username:password] broker_address port qos topic_path client_id back_app_id back_rest_id back_dbname
```
#### Exemplo com Autenticação:
```
python mygarden:123 127.0.0.1 1883 0 /home/horta test 123123123 123123123 sensores
```

#### Exemplo sem Autenticação:
```
python 127.0.0.1 1883 0 /home/horta test 123123123 123123123 sensores
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

# Não obrigatório, caso não seja necessário, deixar em branco.
mqtt_user = usuario de autenticacao
mqtt_passwd = senha de autenticacao
mqtt_qos = Nivel de qualidade de serviço
mqtt_topic = /caminho/para/o/sensor

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
mqtt_server = 127.0.0.1
mqtt_port = 1883
mqtt_ID = TCCREDES
mqtt_user = 
mqtt_passwd = 
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

### Etapa 2 - Execução do arquivo Main:
```
python main.py
```


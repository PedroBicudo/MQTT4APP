"""Inserir informacoes do arquivo .INI na classe Mqtt4app."""
from configparser import ConfigParser
from mqtt4app import Mqtt4App

if __name__ == "__main__":
    auth = None
    file = ConfigParser()
    file.read('mosquitto_config.ini')

    # Configuracoes do servidor
    server = file.get('SERVER_SETTINGS', 'mqtt_server')
    port = file.get('SERVER_SETTINGS', 'mqtt_port')
    id = file.get('SERVER_SETTINGS', 'mqtt_ID')
    user = file.get('SERVER_SETTINGS', 'mqtt_user')
    passwd = file.get('SERVER_SETTINGS', 'mqtt_passwd')
    qos = file.get('SERVER_SETTINGS', 'mqtt_qos')
    topic = file.get('SERVER_SETTINGS', 'mqtt_topic')

    if user and passwd:
        auth = dict(zip(['username', 'password'], [user, passwd]))

    # Back4App
    app_id = file.get('BACK4APP', 'back_app_id')
    rest_id = file.get('BACK4APP', 'back_rest_id')
    class_name = file.get('BACK4APP', 'back_dbname')

    # sensores
    sensors = file.get('SENSORS_SETTINGS', 'sensors').replace(' ', '').split(',')
    micr_ids = file.get('SENSORS_SETTINGS', 'micr_ids').replace(' ', '').split(',')

    # Inserindo valores e conectando
    mqtt4app = Mqtt4App(server, port, qos, 
                        topic, id, app_id, 
                        rest_id, class_name, 
                        sensors, micr_ids
                    )
    mqtt4app.connectToBroker(auth)


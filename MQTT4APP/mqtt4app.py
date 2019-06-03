"""Script responsavel pelo protocolo mqtt e seu envio para o banco de dados."""
from http.client import HTTPSConnection
from paho.mqtt.client import Client
import json


def dataVerify(func):
    """Verificar se os dados existem no arquivo de configuracao."""
    def dataExists3f(self):
        if self.topic and self.mic_id:
            return func(self)
    return dataExists3f


class Mqtt4App(Client):
    """Classe para acesso ao Broker e envio de dados ao Back4App.

    Como usar?

    # Instancia
    mqtt4app = Mqtt4App(
                        broker_address, port, qos,
                        topic_path, client_id, back_app_id,
                        back_rest_id, back_dbname
                        )

    # Efetuar a conexao
    mqtt4app.connectToBroker(auth={'username': username, 'password': passwd})

    # Mostrar dados inseridos
    print(mqtt4app)
    """

    connection = HTTPSConnection(host="parseapi.back4app.com", port=443)

    def __init__(self, broker_address=None, port=1883,
                 qos=0, topic_path=None, client_id=None,
                 back_app_id=None, back_rest_id=None,
                 back_dbname=None, sensors=[], micr_ids=[]
                 ):
        """Obter dados para conexao, monitoramento e envio de dados.

        broker_address: Endereco do servidor Broker
        qos: Nivel de qualidade de servico
        port: Porta usada pelo Broker
        topic_path: Caminho do Topico
        client_id: identificacao da conexao para melhor organizacao
        back_app_id: App ID fornecido pelo Back4App
        back_rest_id: Rest ID fornecido pelo Back4App
        back_dbname: Nome da classe criada no Back4App
        sensors: Lista com o nome do sensor
        micr_ids: Identificacao dos microcontroladores
        """
        path_and_id = topic_path and client_id
        port_and_qos = port.isnumeric() and qos.isnumeric()
        back_requirements = back_app_id and back_rest_id and back_dbname
        assert broker_address, 'Endereco do servidor Broker nao informado.'
        assert isinstance(broker_address, str), 'O broker_address deve ser String.' #NOQA
        assert path_and_id, 'O caminho do topic e o ID devem ser informados.'
        assert port_and_qos, 'A porta e Qos devem ser inteiros.'
        assert back_requirements, 'Os parametros Back4App devem ser inseridos.'
        assert sensors and micr_ids, "Insira o nome dos sensores e microcrontroladores."
        super().__init__()
        self.client_id = client_id
        self.broker_address = broker_address
        self.port = int(port)
        self.qos = int(qos)
        self.topic_path = topic_path if topic_path.endswith('/') else topic_path + '/' #NOQA
        self.sensors = sensors
        self.micr_ids = micr_ids
        self.back_app_id = back_app_id
        self.back_rest_id = back_rest_id
        self.back_dbname = back_dbname
        self.on_connect = self.__subscribeTopics__
        self.on_message = self.__getData__

    def __str__(self):
        """Mostrar informacoes inseridas."""
        return """
        Broker: {}:{}
        Topic Path: {}{}
        Qos: {}
        """.format(self.broker_address, self.port, self.topic_path,
                   self.client_id, self.qos
                   )

    def connectToBroker(self, auth=None):
        """Conectar no servidor Broker.

        Sera verificado se o parametro 'auth' existe para realizar a
        autenticacao, mas caso nao exista, sera desconsiderado na conexao.

        auth: Dicionario de autenticacao
            Estrutura:
            {
                'username': username,
                'password': password
            }

        Tipo de retorno: None
        """
        if auth:
            user_passwd = auth.get('username') and auth.get('password')
            assert user_passwd, 'Usuario ou senha nao informados.'
            self.username_pw_set(**auth)

        self.connect(host=self.broker_address, port=self.port)
        self.loop_forever()

    def __subscribeTopics__(self, client, *args):
        """Realizar a inscricao em topicos.

        client: Instancia Client

        Tipo de retorno: None
        """
        print("Conectado com sucesso.")
        client.subscribe("{}+/+".format(self.topic_path), self.qos)

    def __getData__(self, client, userdata, msg=[]):
        """Obter dados referentes aos topicos e enviar para o banco de dados.

        client: Instancia de client
        msg: Dados referentes aos topicos

        Tipo de retorno: None
        """
        self.current_topic = str(msg.topic)
        self.current_data = int(msg.payload)
        self.__sensorAndMicrocontrollerFilter__()
        self.__sendDataToBack4App__()

    def __sensorAndMicrocontrollerFilter__(self):
        """Buscar sensor no topico recebido.
        
        Tipo de retorno: None
        """
        result = lambda data: None if not data or len(data) > 1 else data[0]
        sensor = list(filter(lambda x: x in self.current_topic, self.sensors))
        id = list(filter(lambda x: x in self.current_topic, self.micr_ids))
        self.topic = result(sensor)
        self.mic_id = result(id)

    @dataVerify
    def __sendDataToBack4App__(self):
        """Enviar os dados obtidos para o Back4App.
        
        Tipo de retorno: None
        """
        
        insert_data = json.dumps(
                                    {
                                        "id": "{}".format(self.client_id),
                                        "topico": "{}".format(self.topic),
                                        "valor": self.current_data
                                    }
                                )

        insert_id = {
                        "X-Parse-Application-Id": self.back_app_id,
                        "X-Parse-REST-API-Key": self.back_rest_id,
                        "Content-Type": "application/json"
                    }

        try:
            classpath = '/classes/{}/'.format(self.back_dbname)
            self.connection.connect()
            self.connection.request('POST', classpath, insert_data, insert_id)
            results = str(json.loads(self.connection.getresponse().read()))
            print('\nTopico recebido: {}'.format(self.current_topic))
            print("Resultado: {}".format(results), end='\n')

        except Exception as error:
            print("Ops alguma coisa aconteceu!")
            print("Tipo de Erro: {}".format(error))


def main(auth=None, *args):
    """Iniciar monitoramento e envio de dados.

    Tipo de retorno: None
    """
    mqtt4app = Mqtt4App(*args)
    mqtt4app.connectToBroker(auth)


if __name__ == "__main__":
    import sys
    howto = """
    Como usar?

    \tpython [username:password] broker_address port qos topic_path client_id back_app_id back_rest_id back_dbname
    """ # NOQA
    args = sys.argv[1:]
    auth = None
    args_vrf = len(args) is 8 or len(args) is 9
    assert args_vrf, "Existem parametros em falta.\n{}".format(howto)

    if ':' in args[0]:
        auth = dict(zip(['username', 'password'], args[0].split(':')))
        del args[0]
    main(auth, *args)

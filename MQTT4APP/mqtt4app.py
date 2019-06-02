"""Script responsavel pelo protocolo mqtt e seu envio para o banco de dados."""
from paho.mqtt.client import Client

class Mqtt4App(Client):
    """Script que conecta, monitora e envia dados obtidos dos topicos do Broker ao Back4App.

    Como usar?
    # Instancia
    mqtt4app = Mqtt4App(auth, broker_address, qos, port, topic_path, client_id, back_app_id, back_rest_id)

    # Efetuar a conexao
    mqtt4app.connectToBroker()

    # Mostrar dados inseridos
    print(mqtt4app)
    """
    
    def __init__(self, auth={}, broker_address=None, port=1883, 
                 qos=0, topic_path=None, client_id=None,
                 back_app_id=None, back_rest_id=None
                ):
        """Obter dados referentes a conexao, monitoramento, autenticacao e envio.
        
        auth: DicionÃ¡rio para efetuar a autenticaÃ§Ã£o
            Estrutura:
                    {
                        'username': user
                        'password': passwd
                    }
        
        broker_address: Endereco do servidor Broker
        qos: Nivel de qualidade de servico
        port: Porta usada pelo Broker
        topic_path: Caminho do TÃ³pico
        client_id: identificacao da conexao para melhor organizacao
        back_app_id: App ID fornecido pelo Back4App
        back_rest_id: Rest ID fornecido pelo Back4App
        """
        assert auth.get('username') and auth.get('password'), 'Usuario ou senha nao informados.'
        assert broker_address, 'EndereÃ§o do servidor Broker nao informado.'
        assert topic_path and client_id, 'O caminho do topic e o ID devem ser informados'
        assert port.isnumeric() and qos.isnumeric(), 'A porta e Qos devem ser inteiros.'
        assert back_app_id and back_rest_id, 'As hashs do Back4App devem ser inseridas.'
        super().__init__()
        self.client_id = client_id
        self.broker_address = broker_address
        self.port = int(port)
        self.qos = int(qos)
        self.auth = auth
        self.topic_path = topic_path if topic_path.endswith('/') else topic_path + '/'
        self.on_connect = self.__subscribeTopics__
        self.on_message = self.__getData__
    
    def __str__(self):
        """Mostrar informacoes inseridas."""
        return """
        Broker: {}:{}
        Topic Path: {}{}
        Qos: {}
        """.format(self.broker_address, self.port, self.topic_path, self.client_id, self.qos)
    
    def connectToBroker(self):
        """Conectar no servidor Broker.
        
        Tipo de retorno: None
        """
        self.username_pw_set(**self.auth)
        self.connect(host=self.broker_address, port=self.port)
        self.loop_forever()

    def __subscribeTopics__(self, client, *args):
        """Realizar a inscricao em topicos.

        client: Instancia Client

        Tipo de retorno: None
        """
        print("Conectado com sucesso.")
        fullTopic = "{}{}".format(self.topic_path, self.client_id)
        client.subscribe(fullTopic, self.qos)
    
    def __getData__(self, client, userdata, msg=[]):
        """Obter dados referentes aos tÃ³picos e enviar para o banco de dados.

        client: Instancia de client
        msg: Dados referentes aos tÃ³picos
        
        Tipo de retorno: None
        """
        topic, payload = msg
        print(topic)
        print(payload)
        

def main(*args):
    """Iniciar monitoramento e envio de dados.
    
    Tipo de retorno: None
    """
    mqtt4app = Mqtt4App(*args)
    print(mqtt4app)
    mqtt4app.connectToBroker()

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    auth = dict(zip(['username', 'password'], args[0].split(':')))
    args[0] = auth
    if len(auth) is not 2 or len(args) is not 8:
        print("""
        Como usar?

        python -m username:password broker_address qos port topic_path client_id back_app_id back_rest_id
        """)
        sys.exit(1)
    
    print(args)
    print(auth)
    main(*args)
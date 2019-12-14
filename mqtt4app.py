"""Classe responsavel por executar o projeto."""
from http.client import HTTPSConnection
from paho.mqtt.client import Client
import json


class Mqtt4App(Client):
    """Classe de monitoramento e envio de informacoes ao back4app."""

    BACK4APP_CON = HTTPSConnection(host="parseapi.back4app.com", port=443)

    def __init__(self, back_db_name=None, back_app_id=None, back_rest_id=None,
                 topics=[], qos=0, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.back_app_id = back_app_id
        self.back_rest_id = back_rest_id
        self.back_db_name = back_db_name
        self.qos = qos
        self.topics = self._convert_to_tuple_list(topics)
        self.con_id = self.get_json_connection_id()
        self.classpath = self._get_class_path()

    def _convert_to_tuple_list(self, topics):
        """Modificar uma lista de topicos para uma lista de tuplas."""
        new_topics = []
        for topic in topics:
            new_topics.append((topic, self.qos))

        return new_topics

    def start_connection(self, address, port):
        """Inicia conexao com o Broker.

        Parameters
        ----------
        address: str
            Endereco do servidor Broker.

        """
        msg = f"Conexao com {address}:{port} estabelecida com sucesso."
        self.connect(address, port)
        self.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        """Realiza a inscricao de topicos."""
        msg = (
            f"{len(self.topics)} foram cadastrados "
            f"na conexao {client._host}."
        )
        client.subscribe(self.topics)

    def on_disconnect(self, client, userdata, rc):
        """Realiza a reconexao, caso se torne indisponivel."""
        msg = f"A conexao com {self._host} foi perdida, reconectando..."
        client.reconnect()

    def on_message(self, client, userdata, msg):
        """Manipula a mensagem e o topico."""
        payload = float(msg.payload)
        topic = msg.topic
        print(topic, payload)
        json_data = self.get_json_data(payload, topic)
        self._send_data_to_back4app(json_data)

    def get_json_data(self, payload, topic):
        """Gerar JSON com a estrutura de envio para o trabalho."""
        return json.dumps(
                         {
                            "topic": f"{topic}",
                            "payload": payload
                         }
        )

    def get_json_connection_id(self):
        """Informacoes essenciais para a conexao com o Back4App."""
        return {
                    "X-Parse-Application-Id": self.back_app_id,
                    "X-Parse-REST-API-Key": self.back_rest_id,
                    "Content-Type": "application/json"
               }

    def _get_class_path(self):
        return f'/classes/{self.back_db_name}/'

    def _send_data_to_back4app(self, data):
        """Realizar conexao com o back4app.

        Parameters
        ----------
        classpath: str
            Localizacao do banco NoSQL.

        data: JSON
            JSON com informacoes relacionadas ao topico.
            ex: {"topico": "abc", "valor": 123}

        """
        back_ids = self.back_app_id and self.back_rest_id
        if not back_ids or not self.back_db_name:
            return

        try:
            self.BACK4APP_CON.connect()
            self.BACK4APP_CON.request(
                'POST',
                self.classpath,
                data,
                self.con_id
            )
            response = json.loads(self.BACK4APP_CON.getresponse().read())
            print(response)

        except ConnectionRefusedError as err:
            print("A conexao foi recusada: ", err)

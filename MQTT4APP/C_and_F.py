'''
Escrito: SRKFY
Data: 30/11/2018
Nome: C_and_F.py
Função:
    -> Filtragem e tratamento de informações
    
'''
import json, http.client
from mosquitto_config import *

class Msteps():

    def __init__(self, topico, valor, back_app_id, back_rest_id):
        self.topico = topico
        self.valor = valor
        self.back_app_id = back_app_id
        self.back_rest_id = back_rest_id

    def filtro_id(self):
        for numid in range(len(mic_id)):
            if mic_id[numid] in self.topico:
                self._id = mic_id[numid]
                print(mic_id[numid])
                break
            else:
                pass

    def sensor(self):
       for nums in range(len(mic_sensors)):
            if mic_sensors[nums] in self.topico:
                print(mic_sensors[nums])
                self.topico=mic_sensors[nums]
                break
            else:
                pass
    
    def connect_back4app(self):
        insert_data = json.dumps({
            "id": "%s" % self._id, 
            "topico": "%s" % self.topico,
            "valor": self.valor
        })

        insert_id = {
            "X-Parse-Application-Id": self.back_app_id,
            "X-Parse-REST-API-Key": self.back_rest_id,
            "Content-Type": "application/json"
        }

        try:
            connection = http.client.HTTPSConnection("parseapi.back4app.com", 443)
            connection.connect()
            connection.request('POST', '/classes/sensor/', insert_data, insert_id)
            results = str(json.loads(connection.getresponse().read()))
            print("\t%s" %results)

        except Exception as error:
            print(
                "Ops alguma coisa aconteceu!\n", 
                "Tipo de Erro:", error)



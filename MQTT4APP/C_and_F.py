'''

Escrito: SRKFY
Data: 30/11/2018
Nome: C_and_F.py

Função:
    -> Filtragem e tratamento de informações
    
'''
import json, http.client

class Msteps():

    def __init__(self, topico, valor, back_app_id, back_rest_id):
        self.topico = topico
        self.valor = valor
        self.back_app_id = back_app_id
        self.back_rest_id = back_rest_id

    def filtro_id(self):
        for id_e in range(0, len(self.topico)):
            if self.topico[id_e:id_e+3] == "id_":
                self.posicao = id_e+3
                break

        for id_b in range(self.posicao, len(self.topico)):
            if self.topico[id_b:id_b+1] == "/":
                self._id = self.topico[self.posicao:id_b]
                break
        
    def sensor(self):
        for sensor in range(1, len(self.topico)):
                if self.topico[sensor:sensor+7] == "umidade":
                    self.topico ="umidade"
                    break
                if self.topico[sensor:sensor+11] == "temperatura":
                    self.topico ="temperatura"
                    break
                if self.topico[sensor:sensor+12] == "luminosidade":
                    self.topico ="luminosidade"
                    break
    
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


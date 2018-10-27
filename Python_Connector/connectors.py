import json, http.client
from mosquitto_config import \
    back_app_id, \
    back_rest_id

def connect_back4app(_id, topico, valor):

    insert_data = json.dumps({
        "id": "%s" % _id, 
        "topico": "%s" % topico, 
        "valor": valor 
    })

    insert_id = {
        "X-Parse-Application-Id": back_app_id,
        "X-Parse-REST-API-Key": back_rest_id,
        "Content-Type": "application/json"
        }

    try:
        connection = http.client.HTTPSConnection("parseapi.back4app.com", 443)
        connection.connect()
        connection.request('POST', '/classes/sensor/', insert_data, insert_id
        )
        results = json.loads(connection.getresponse().read())
        print(results)
    except NameError:
        print("Erro na conexao")



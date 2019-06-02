# Simulador de sensores

## Qual a função do arquivo?
<p> O arquivo mqttpublish tem a função de enviar valores aleatórios ao Broker para testes de funcionamento</p>

## Quais os tipos de sensores que enviaram os dados aleatórios?
- temperatura;
- umidade;
- luminosidade.

## Como usar o mqttpublish?
```
python mqttpublish.py  [topico] [ID] [intervalo] [broker_ip] [port] [usuario] [senha]
```

### Exemplo de uso:
```
python mqttpublish.py /home/horta/ teste 10.0 127.0.0.1 1883 mygarden 123
```

## Estrutura dos tópicos:
|   caminho   |   ID  | tipo de sensor |
|-------------|-------|----------------|
| /home/horta | teste | temperatura    |

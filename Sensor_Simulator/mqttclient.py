import paho.mqtt.publish as mqtt
import random as rd
import time as tm

def logo():
    print("""
==========================================================================
=	 ____  _____ _   _ ____   ___  ____                              =
=	/ ___|| ____| \ | / ___| / _ \|  _ \                             =
=	\___ \|  _| |  \| \___ \| | | | |_) |                            =
=	 ___) | |___| |\  |___) | |_| |  _ <                             =
=	|____/|_____|_| \_|____/ \___/|_| \_\                            =
=                                                                        =
=           ____ ___ __  __ _   _ _        _  _____ ___  ____            =
=           / ___|_ _|  \/  | | | | |      / \|_   _/ _ \|  _ \          =
=           \___ \| || |\/| | | | | |     / _ \ | || | | | |_) |         =
=            ___) | || |  | | |_| | |___ / ___ \| || |_| |  _ <          =
=           |____/___|_|  |_|\___/|_____/_/   \_\_| \___/|_| \_\         =
=                                                                        =
==========================================================================

--------------------------------------------------------------------------
INICIANDO...
--------------------------------------------------------------------------
    """)
    tm.sleep(5.0)

mqtt_ID="SENSOR-PUB"
logo()
while True:
    valores=rd.sample(range(0,100), 4)
    msgs=[{
        'topic':'/home/horta/%s/temperatura' % mqtt_ID,
        'payload': '%d' % valores[1]
    },{
        'topic':'/home/horta/%s/umidade' % mqtt_ID,
        'payload': '%d' % valores[2]
   },
    {
        'topic':'/home/horta/%s/luminosidade' % mqtt_ID,
        'payload': '%d' % valores[3]
    }]

    # PUBLISH + AUTH 
    mqtt.multiple(msgs, hostname='127.0.0.1', port=1883, client_id=mqtt_ID, auth={'username': 'mygarden', 'password': '123'} )
    print(msgs)
    tm.sleep(10.0)

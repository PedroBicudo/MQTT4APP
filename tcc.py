"""Inserir informacoes do arquivo .INI na classe Mqtt4app."""
from string import ascii_letters
from mqtt4app import Mqtt4App
from random import choices
import argparse


def remove_none_values(data):
    """Eliminar valores nulos no dicionario.

    Parameters
    ----------
    data: dict
        Dicionario de argumentos.

    Returns
    ----------
    dict
        Dicionario sem valores None.

    """
    new_data = {}
    for index, value in data.items():
        if not value and value != 0:
            continue
        new_data[index] = value

    return new_data


def get_parser():
    """Obter parser relativo ao projeto.

    Returns
    ----------
    argparse.ArgumentParser
        Parser do projeto.

    """
    return argparse.ArgumentParser(
        description="Projeto TCC SENAI DE REDES"
    )


def load_essential_params(parser):
    """Carregar os parametros essenciais para o funcionamento do protocolo."""
    essentials = parser.add_argument_group("Parametro Obrigatorio")
    essentials.add_argument(
        "-server",
        help="Endereço de IP do Servidor MQTT.",
        dest="mqtt_server",
        required=True,
    )

    # Adicionar opcao de arquivo
    essentials.add_argument(
        "-topics", "-T",
        nargs="*",
        help="Topico(s) a ser(em) monitorado(s).",
        required=True
    )

    essentials.add_argument(
        "-backid", "-Bi",
        help="Back4app ID"
    )

    essentials.add_argument(
        "-backrest", "-Br",
        help="Back4app REST"
    )

    essentials.add_argument(
        "-backdb", "-Bdb",
        help="Nome do banco de dados Back4app."
    )


def load_non_essential_params(parser):
    """Carregar os parametros nao obrigratorios para o usuario."""
    non_essential = parser.add_argument_group("Parametros nao obrigatorios")
    non_essential.add_argument(
        "-port",
        help="Porta utilizada pelo servidor MQTT.",
        dest="mqtt_port",
        type=int,
        default=1883
    )
    non_essential.add_argument(
        "-clientid",
        help="Identificacao da conexao.",
        type=str,
        default=None
    )
    non_essential.add_argument(
        "-user", "-U",
        help="Usuario para acesso.",
        type=str
    )
    non_essential.add_argument(
        "-passw", "-P",
        help="Senha de acesso.",
        type=str
    )
    non_essential.add_argument(
        "-qos", "-Q",
        help="Nivel de qualidade de servico.",
        type=int,
        default=1
    )
    non_essential.add_argument(
        "-transport", "-Tr",
        help="Protocolo de transporte",
        type=str
    )


def main():
    """Inicializar o argparser."""
    parser = get_parser()
    load_essential_params(parser)
    load_non_essential_params(parser)
    result = remove_none_values(parser.parse_args().__dict__)
    server, port = result['mqtt_server'], result['mqtt_port']
    result.pop('mqtt_server')
    result.pop('mqtt_port')
    mqtt4app = Mqtt4App(**result)
    mqtt4app.start_connection(server, port)


if __name__ == "__main__":
    main()

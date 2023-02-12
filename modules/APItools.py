import requests


def get_route(solar_system_id_from: int, solar_system_id_to: int, security_mode: str):
    request_str = f'https://esi.evetech.net/latest/route/{solar_system_id_from}/{solar_system_id_to}/?datasource=tranquility&flag={security_mode}'

    response = requests.get(request_str)
    while response.status_code != 200:
        response = requests.get(request_str)

    return response.json()


def get_system_kills():
    request_str = f'https://esi.evetech.net/latest/universe/system_kills/?datasource=tranquility'

    response = requests.get(request_str)
    while response.status_code != 200:
        response = requests.get(request_str)

    return response.json()

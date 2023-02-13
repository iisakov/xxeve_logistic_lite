import requests
import inspect


def c_request(request_str):
    headers = {'Accept': 'gzip',
               'User-Agent': 'iisakov.artisan@yandex.ru. Maintainer: https://github.com/iisakov/xxeve_logistic_lite'}
    response = requests.get(url=request_str, headers=headers)
    print(inspect.stack()[1][3], response.status_code)
    while response.status_code != 200:
        print(inspect.stack()[1][3], response.status_code)
        response = requests.get(url=request_str, headers=headers)

    return response.json()


# API ESI
def get_route(solar_system_id_from: int, solar_system_id_to: int, security_mode: str):
    request_str = f'https://esi.evetech.net/latest/route/{solar_system_id_from}/{solar_system_id_to}/?datasource=tranquility&flag={security_mode}'
    return c_request(request_str)


def get_system_kills():
    request_str = f'https://esi.evetech.net/latest/universe/system_kills/?datasource=tranquility'
    return c_request(request_str)


def get_system_jumps():
    request_str = f'https://esi.evetech.net/latest/universe/system_jumps/?datasource=tranquility'
    return c_request(request_str)


def get_killmail_by_killmail_key(killmail_id, killmail_hash):
    request_str = f'https://esi.evetech.net/latest/killmails/{killmail_id}/{killmail_hash}/?datasource=tranquility'
    return c_request(request_str)


# API zKillboard
def get_stats_kills_system_from_zkillboard(solar_system_id):
    request_str = f'https://zkillboard.com/api/stats/solarSystemID/{solar_system_id}/'
    return c_request(request_str)


def get_killmail_by_solar_system_id(solar_system_id):
    request_str = f'https://zkillboard.com/api/kills/solarSystemID/{solar_system_id}/pastSeconds/3600/'
    return c_request(request_str)


# Отключено из-за злоупотреблений
def get_killmail_by_many_solar_system_id(solar_system_id_list):
    request_str = f'https://zkillboard.com/api/kills/solarSystemID/{",".join([str(x) for x in solar_system_id_list])}/'
    return c_request(request_str)

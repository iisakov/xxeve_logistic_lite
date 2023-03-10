import json
import time
import asyncio

from itertools import chain
from time import sleep

from . import SQLtools
from . import APItools
from . import asyncAPItools
from . import STL
from . import viewer

from pprint import pprint as pp

#TODO Организовать из полученных данных удобный CLI интерфейс.


def run(argv, main_cli_param):
    time_start = time.time()

    security_mode = argv['scm']                                     # Модификатор безопасности маршрута
    solar_system_from = argv['scf']                                 # Название Начальной звёздной системы
    solar_system_to = argv['sct']                                   # Название конечной звёздной системы
    solar_system_list = [solar_system_from, solar_system_to]        # Список названий звёздных систем

    print('Получаем сведения о начальной и конечной звёдных системах.')
    # Получаем сведения о начальной и конечной звёдных системах.
    solar_systems = SQLtools.get_many_solar_system_by_name(conn=SQLtools.get_conn(),
                                                           solar_system_name_list=solar_system_list)

    solar_system_list = list(solar_systems)
    solar_system_from = solar_system_list[0]
    solar_system_to = solar_system_list[1]

    print('Получаем оптимальный маршрут (список solarSystemID).')
    # Получаем оптимальный маршрут (список solarSystemID).
    optimize_route = APItools.get_route(solar_system_id_from=solar_systems[solar_system_from]['solarSystemID'],
                                        solar_system_id_to=solar_systems[solar_system_to]['solarSystemID'],
                                        security_mode=security_mode)

    print('Получаем информацию о всех звёздных системах, входящих в маршрут.')
    # Получаем информацию о всех звёздных системах.
    solar_systems = SQLtools.get_many_solar_system_by_id(conn=SQLtools.get_conn(),
                                                         solar_system_id_list=optimize_route)

    print('Добавляем (перезаписываем) промежуточные названия звёздных систем.')
    # Добавляем (перезаписываем) промежуточные названия звёздных систем.
    solar_system_name_list = list(solar_systems.keys())

    print('Получаем список звёздных врат по каждой системе.')
    # Получаем список звёздных врат по каждой системе.
    solar_systems_stargate = SQLtools.get_all_stargate_by_many_solar_system_id(conn=SQLtools.get_conn(),
                                                                               solar_system_id_list=optimize_route)
    for solar_system_name, solar_system_stargate in solar_systems_stargate.items():
        solar_systems[solar_system_name]['stargate'] = solar_system_stargate

    print('Получаем список всех доступных объектов по каждой системе.')
    # Получаем список всех доступных объектов по каждой системе.
    solar_systems_object = SQLtools.get_all_objects_by_many_solar_system_id(conn=SQLtools.get_conn(),
                                                                            solar_system_id_list=optimize_route)
    for solar_system_name, solar_system_values in solar_systems_object.items():
        solar_systems[solar_system_name]['object'] = solar_system_values

    print('Получаем снимок убийств за последний час.')
    # Получаем снимок убийств за последний час.
    for solar_system_key, solar_system_values in solar_systems.items():
        solar_system_values['kills'] = {'npc_kills': 0, 'pod_kills': 0, 'ship_kills': 0}

    for solar_system_kill in APItools.get_system_kills():
        for solar_system_key, solar_system_values in solar_systems.items():
            if solar_system_kill['system_id'] == solar_system_values['solarSystemID']:
                solar_system_values['kills'] = solar_system_kill
                break

    print('Получаем снимок прыжков за последний час.')
    # Получаем снимок прыжков за последний час.
    for solar_system_jump in APItools.get_system_jumps():
        for solar_system_key, solar_system_values in solar_systems.items():
            if solar_system_jump['system_id'] == solar_system_values['solarSystemID']:
                solar_systems[solar_system_key]['jump'] = solar_system_jump

    print('Получаем убойные письма с сайта zKillboard')
    # Получаем убойные письма с сайта zKillboard
    region_id = {solar_system['regionID'] for solar_system in solar_systems.values()}
    killmail_list_from_zkb = list(chain(*asyncio.run(asyncAPItools.get_killmail_by_many_region_id(region_id))))
    killmail_list_from_esi = asyncio.run(asyncAPItools.get_killmails_by_killmail_keys([(i['killmail_id'], i['zkb']['hash']) for i in killmail_list_from_zkb]))
    for killmail_from_zkb in killmail_list_from_zkb:
        for killmail_from_esi in killmail_list_from_esi:
            if killmail_from_zkb['killmail_id'] == killmail_from_esi['killmail_id']:
                for solar_system_key, solar_system_value in solar_systems.items():
                    if 'killmails' not in solar_system_value:
                        solar_system_value['killmails'] = []
                    if killmail_from_esi['solar_system_id'] in solar_system_key:
                        solar_system_value['killmails'].append(killmail_from_zkb | killmail_from_esi)

    print('Получаем информацию о кораблях в убойных письмах.')
    # Получаем информацию о кораблях в убойных письмах.
    for solar_system_key, solar_system_values in solar_systems.items():
        if 'killmails' not in solar_system_values:
            continue
        for i, killmail in enumerate(solar_systems[solar_system_key]['killmails']):
            for attacker in killmail['attackers']:
                if 'ship_type_id' in attacker:
                    attacker['ship'] = SQLtools.get_entity_by_tipe_id(conn=SQLtools.get_conn(),
                                                                      tipe_id=attacker['ship_type_id'])
            if 'ship_type_id' in killmail['victim']:
                killmail['victim']['ship'] = SQLtools.get_entity_by_tipe_id(conn=SQLtools.get_conn(),
                                                                            tipe_id=killmail['victim']['ship_type_id'])

    print('Получаем ближайший к убийству объект и звёздные врата.')
    # Получаем ближайший к убийству объект и звёздные врата.
    for key, values in solar_systems.items():
        if 'killmails' not in values:
            continue
        for killmail in values['killmails']:
            killmail['nearest_stargate'] = STL.get_nearest_point(point_from=tuple(killmail['victim']['position'].values()),
                                                                 points_to={stargate['stargateName']: (stargate['x'], stargate['y'], stargate['z']) for stargate in values['stargate']})
            killmail['nearest_object'] = STL.get_nearest_point(point_from=tuple(killmail['victim']['position'].values()),
                                                               points_to={object['objectName']: (object['x'], object['y'], object['z']) for object in values['object']})

    print(time.time() - time_start)
    viewer.view_security_check_data(solar_systems, optimize_route)


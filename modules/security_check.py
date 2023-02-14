from time import sleep

from . import SQLtools
from . import APItools
from . import STL

from pprint import pprint as pp


# TODO По координатам высчитать близость убийств к звёздным вратам.
# TODO Организовать из полученных данных удобный CLI интерфейс.


def run(argv, main_cli_param):
    security_mode = argv['scm']                                                 # Модификатор безопасности маршрута
    solar_system_name_from = argv['scf']                                        # Название Начальной звёздной системы
    solar_system_name_to = argv['sct']                                          # Название конечной звёздной системы
    solar_system_name_list = [solar_system_name_from, solar_system_name_to]     # Список названий звёздных систем

    print('Получаем сведения о начальной и конечной звёдных системах.')
    # Получаем сведения о начальной и конечной звёдных системах.
    solar_systems = SQLtools.get_many_solar_system_by_name(conn=SQLtools.get_conn(),
                                                           solar_system_name_list=solar_system_name_list)

    print('Получаем оптимальный маршрут (список solarSystemID).')
    # Получаем оптимальный маршрут (список solarSystemID).
    optimize_route = APItools.get_route(solar_system_id_from=solar_systems[solar_system_name_from]['solarSystemID'],
                                        solar_system_id_to=solar_systems[solar_system_name_to]['solarSystemID'],
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

    print('Получаем снимок убийств за последний час.')
    # Получаем снимок убийств за последний час.
    for solar_system_kill in APItools.get_system_kills():
        for solar_system_key, solar_system_values in solar_systems.items():
            if solar_system_kill['system_id'] == solar_system_values['solarSystemID']:
                solar_systems[solar_system_key]['kills'] = solar_system_kill

    print('Получаем снимок прыжков за последний час.')
    # Получаем снимок прыжков за последний час.
    for solar_system_jump in APItools.get_system_jumps():
        for solar_system_key, solar_system_values in solar_systems.items():
            if solar_system_jump['system_id'] == solar_system_values['solarSystemID']:
                solar_systems[solar_system_key]['jump'] = solar_system_jump

    print('Получаем убойные письма с сайта zKillboard')
    # Получаем убойные письма с сайта zKillboard
    for solar_system_key, solar_system_values in solar_systems.items():
        solar_systems[solar_system_key]['killmails'] = APItools.get_killmail_by_solar_system_id(solar_system_values['solarSystemID'])
        sleep(2)

    print('Получаем и дописываем инфу по убойным письмам от ESI.')
    # Получаем и дописываем инфу по убойным письмам от ESI.
    for solar_system_key, solar_system_values in solar_systems.items():
        for i, killmail in enumerate(solar_systems[solar_system_key]['killmails']):
            solar_systems[solar_system_key]['killmails'][i] = killmail | APItools.get_killmail_by_killmail_key(killmail_id=killmail['killmail_id'],
                                                                                                               killmail_hash=killmail['zkb']['hash'])

    print('Получаем информацию о кораблях в убойных письмах.')
    # Получаем информацию о кораблях в убойных письмах.
    for solar_system_key, solar_system_values in solar_systems.items():
        for i, killmail in enumerate(solar_systems[solar_system_key]['killmails']):
            for attacker in killmail['attackers']:
                attacker['ship'] = SQLtools.get_entity_by_tipe_id(conn=SQLtools.get_conn(),
                                                                  tipe_id=attacker['ship_type_id'])
            killmail['victim']['ship'] = SQLtools.get_entity_by_tipe_id(conn=SQLtools.get_conn(),
                                                                        tipe_id=killmail['victim']['ship_type_id'])

    print(STL.linear_distance_between_many_points(*[(solar_system_values['x'], solar_system_values['y'], solar_system_values['z']) for solar_system_key, solar_system_values in solar_systems.items()]))

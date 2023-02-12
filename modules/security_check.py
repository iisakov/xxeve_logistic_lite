from . import SQLtools
from . import APItools

from pprint import pprint as pp

# TODO Получать данные с https://github.com/zKillboard/zKillboard/wiki/API-(Statistics)

def run(argv, main_cli_param):
    security_mode = argv['scm']                                                 # Модификатор безопасности маршрута
    solar_system_name_from = argv['scf']                                        # Название Начальной звёздной системы
    solar_system_name_to = argv['sct']                                          # Название конечной звёздной системы
    solar_system_name_list = [solar_system_name_from, solar_system_name_to]     # Список названий звёздных систем

    # Получаем сведения о звёдных системах.
    solar_systems = SQLtools.get_many_solar_system_by_name(conn=SQLtools.get_conn(),
                                                           solar_system_name_list=solar_system_name_list)

    optimize_route = APItools.get_route(solar_system_id_from=solar_systems[solar_system_name_from]['solarSystemID'],
                                        solar_system_id_to=solar_systems[solar_system_name_to]['solarSystemID'],
                                        security_mode=security_mode)

    solar_systems = SQLtools.get_many_solar_system_by_id(conn=SQLtools.get_conn(),
                                                         solar_system_id_list=optimize_route)

    solar_system_name_list = list(solar_systems.keys())

    solar_systems['Jita']['stargates'] = SQLtools.get_all_stargate_by_solar_system_id(conn=SQLtools.get_conn(),
                                                                                      solar_system_id=solar_systems['Jita']['solarSystemID'])

    for solar_system_kill in APItools.get_system_kills():
        for solar_system_key, solar_system_values in solar_systems.items():
            if solar_system_kill['system_id'] == solar_system_values['solarSystemID']:
                solar_systems[solar_system_key]['kills'] = solar_system_kill

    print(solar_systems['Jita'])

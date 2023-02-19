import datetime
from pprint import pp

from . import VIEWERtools

def view_security_check_data(data, optimize_route):
    data = {value['solarSystemID']: value for key, value in data.items()}

    normaling_str = '\033[01;37m'
    dangerousing_str = '\033[01;36;41m'
    warning_str = '\033[01;33m'
    headering_str = '\033[01;42m'
    nulling_str = '\033[00m'
    haulers = ['Venture', 'Badger', 'Tayra', 'Nereus', 'Hoarder', 'Mammoth', 'Wreathe', 'Kryos', 'Epithal', 'Miasmos', 'Iteron Mark V', 'Bestower', 'Primae', 'Noctis', 'Miasmos Quafe Ultra Edition', 'Miasmos Quafe Ultramarine Edition', 'Sigil', 'Miasmos Amastris Edition', 'Iteron Inner Zone Shipping Edition', 'Tayra Wiyrkomi Edition', 'Mammoth Nefantar Edition', 'Bestower Tash-Murkon Edition', 'Bustard', 'Occator', 'Mastodon', 'Impel', 'Covetor', 'Retriever', 'Procurer', 'Rhea', 'Nomad', 'Anshar', 'Ark']
    header = {'data': ['solar_system_name', 'npc_kills', 'pod_kills', 'ship_kills', 'num_killmal']}
    sub_header = {'data': ['killmail_time', 'stargate_name', 'distances', 'victim ship', 'attakers sips']}

    table = {'header': header,
             'rows': []}
    for num_row, solar_system_id in enumerate(optimize_route):
        table['rows'].append({'data':[data[solar_system_id]['solarSystemName'],
                                      data[solar_system_id]['kills']['npc_kills'],
                                      data[solar_system_id]['kills']['pod_kills'],
                                      data[solar_system_id]['kills']['ship_kills'],
                                      len(data[solar_system_id]['killmails'])]})

        for killmail in data[solar_system_id]['killmails']:
            if 'sub_table' not in table['rows'][num_row]:
                table['rows'][num_row]['sub_table'] = {'header': sub_header,
                                                       'rows': []}

            table['rows'][num_row]['sub_table']['rows'].append({'data':[killmail['killmail_time'],
                                                                        killmail['nearest_stargate']['point_to'],
                                                                        killmail['nearest_stargate']['distances'],
                                                                        killmail['victim']['ship']['typeName'],
                                                                        ', '.join([x['ship']['typeName'] for x in killmail['attackers'] if 'ship' in x])]})

    VIEWERtools.create_table(table['header'], table['rows'])
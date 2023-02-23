import datetime
import json
from pprint import pp

from . import VIEWERtools


def view_security_check_data(data, optimize_route):
    data = {value['solarSystemID']: value for key, value in data.items()}

    ship_types = ['Venture', 'Badger', 'Tayra', 'Nereus', 'Hoarder', 'Mammoth', 'Wreathe', 'Kryos', 'Epithal',
                  'Miasmos', 'Iteron Mark V', 'Bestower', 'Primae', 'Noctis', 'Miasmos Quafe Ultra Edition',
                  'Miasmos Quafe Ultramarine Edition', 'Sigil', 'Miasmos Amastris Edition',
                  'Iteron Inner Zone Shipping Edition', 'Tayra Wiyrkomi Edition', 'Mammoth Nefantar Edition',
                  'Bestower Tash-Murkon Edition', 'Bustard', 'Occator', 'Mastodon', 'Impel', 'Covetor',
                  'Retriever', 'Procurer', 'Rhea', 'Nomad', 'Anshar', 'Ark']

    header = {'data': ['solar_system_name', 'npc_kills', 'pod_kills', 'ship_kills', 'num_killmal']}
    sub_header = {'data': ['killmail_time', 'object_name', 'distances', 'victim ship', 'npc']}
    table = {'header': header,
             'rows': []}

    for num_row, solar_system_id in enumerate(optimize_route):
        table['rows'].append({'data': [data[solar_system_id]['solarSystemName'],
                                       data[solar_system_id]['kills']['npc_kills'],
                                       data[solar_system_id]['kills']['pod_kills'],
                                       data[solar_system_id]['kills']['ship_kills'],
                                       len(data[solar_system_id]['killmails'])]})

        for killmail in data[solar_system_id]['killmails']:
            if 'sub_table' not in table['rows'][num_row]:
                table['rows'][num_row]['sub_table'] = {'header': sub_header, 'rows': []}

            sub_row = {'data': [killmail['killmail_time'],
                       killmail['nearest_object']['point_to'] if len(killmail['nearest_object']['point_to']) < 20 else killmail['nearest_object']['point_to'][:20] + '...',
                       killmail['nearest_object']['distances'],
                       killmail['victim']['ship']['typeName'],
                       killmail['zkb']['npc']
                       ]}

            if 99 in [attacker['ship']['groupID'] for attacker in killmail['attackers'] if 'ship' in attacker]:
                sub_row['mode'] = 'warning'

            if 1000125 in [attacker['corporation_id'] for attacker in killmail['attackers'] if 'corporation_id' in attacker]:
                sub_row['mode'] = 'not_npc'

            if killmail['victim']['ship']['typeName'] in ship_types:
                sub_row['mode'] = 'dangerous'

            table['rows'][num_row]['sub_table']['rows'].append(sub_row)

    json.dump(table, open('test.json', 'w'))
    VIEWERtools.create_table(table['header'], table['rows'])

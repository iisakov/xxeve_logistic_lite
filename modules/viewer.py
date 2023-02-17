def view_security_check_data(data):
    dangerousing_str = '\033[01;31;41m'
    warning_str = '\033[01;33m'
    headering_str = '\033[01;42m'
    nulling_str = '\033[00m'
    haulers = ['typeName', 'Badger', 'Tayra', 'Nereus', 'Hoarder', 'Mammoth', 'Wreathe', 'Kryos', 'Epithal', 'Miasmos', 'Iteron Mark V', 'Bestower', 'Primae', 'Noctis', 'Miasmos Quafe Ultra Edition', 'Miasmos Quafe Ultramarine Edition', 'Sigil', 'Miasmos Amastris Edition', 'Iteron Inner Zone Shipping Edition', 'Tayra Wiyrkomi Edition', 'Mammoth Nefantar Edition', 'Bestower Tash-Murkon Edition', 'Bustard', 'Occator', 'Mastodon', 'Impel', 'Covetor', 'Retriever', 'Procurer', 'Rhea', 'Nomad', 'Anshar', 'Ark']
    header = ['solar_system_name', 'npc_kills', 'pod_kills', 'ship_kills', 'num_killmal']
    sub_header = ['stargate_name', 'distances', 'victim ship', 'attakers sips', '']
    for solar_system_key, solar_system_values in data.items():
        print(f"{headering_str}|{header[0]:^20}"
              f"|{header[1]:^20}"
              f"|{header[2]:^20}"
              f"|{header[3]:^20}"
              f"|{header[4]:^20}|{nulling_str}")
        print(f"| {solar_system_key:<19}"
              f"|{solar_system_values['kills']['npc_kills']:^20}"
              f"|{solar_system_values['kills']['pod_kills']:^20}"
              f"|{solar_system_values['kills']['ship_kills']:^20}"
              f"|{len(solar_system_values['killmails']):^20}|")
        print(''.join(['-']*len(header)*20)+'------')
        for killmail in solar_system_values['killmails']:
            print(f"{warning_str if not killmail['zkb']['npc'] else ''}|{sub_header[-1]:^20}"
                  f"|{headering_str}{sub_header[0]:^20}"
                  f"|{sub_header[1]:^20}"
                  f"|{sub_header[2]:^20}"
                  f"|{sub_header[3]:^20}|{nulling_str}")
            print(f"|{warning_str if not killmail['zkb']['npc'] else ''}{sub_header[-1]:^20}"
                  f"| {killmail['nearest_stargate']['point_to']:<19}"
                  f"| {killmail['nearest_stargate']['distances']:<19}"
                  f"| {dangerousing_str if killmail['victim']['ship']['typeName'] in haulers else ''}{killmail['victim']['ship']['typeName']:<19}"
                  f"| {', '.join([x['ship']['typeName'] for x in killmail['attackers'] if 'ship' in x]):<19}|{nulling_str}")
        print(''.join(['-']*len(header)*20)+'------')

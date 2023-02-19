import colorama

mode_str = {'normal':       {'header':  colorama.Back.GREEN + colorama.Fore.LIGHTWHITE_EX,
                             'row':     colorama.Fore.LIGHTWHITE_EX},
            'dangerous':    {'header':  colorama.Back.RED + colorama.Fore.LIGHTWHITE_EX,
                             'row':     colorama.Fore.LIGHTRED_EX},
            'warning':      {'header':  colorama.Back.YELLOW + colorama.Fore.LIGHTWHITE_EX,
                             'row':     colorama.Fore.LIGHTYELLOW_EX},
            'nulling':       colorama.Style.RESET_ALL}


def print_header(header_field: list, col_space: int, mode: str = 'normal'):

    print(mode_str[mode]['header'] + '|', end='')
    for col in header_field:
        print(f'{col:^{col_space}}', end='|')
    print(mode_str['nulling'])


def print_row(row_field: list, col_space: int, mode: str = 'normal'):
    print(mode_str[mode]['row'] + '|', end='')
    for col in row_field:
        print(f'{str(col):^{col_space}}', end='|')
    print(mode_str['nulling'])


def print_offset(num_offset, col_space: int):
    empty_str = ''
    for offset in range(num_offset):
        print(f'{empty_str:^{col_space+1}}', end='')


def print_end_section(num_cols: int, col_space: int):
    print(mode_str['normal']['row'] + ''.join(['-']*col_space*num_cols)+''.join(['-']*num_cols)+'-' + mode_str['nulling'])


def create_table(header: dict, rows: list, **kwargs):
    current_offset = kwargs['offset'] if 'offset' in kwargs else 0
    max_len = 0
    num_field = len(header['data'])

    def count_len(table, max_len):
        for header_field in table['header']['data']:
            max_len = len(header_field) if len(header_field) > max_len else max_len

        for row in table['rows']:
            for row_field in row['data']:
                max_len = len(str(row_field)) if len(str(row_field)) > max_len else max_len
                if 'sub_table' in row:
                    max_len = count_len(table={'header': row['sub_table']['header'],
                                               'rows': row['sub_table']['rows']},
                                        max_len=max_len)
        return max_len

    max_len = count_len({'header': header, 'rows': rows}, max_len)

    print_offset(current_offset, max_len+2)
    print_header(header_field=header['data'],
                 col_space=max_len+2,
                 mode=header['mode'] if 'mode' in header else 'normal')

    for row in rows:
        print_offset(current_offset, max_len + 2)
        print_row(row_field=row['data'],
                  col_space=max_len+2,
                  mode=row['mode'] if 'mode' in row else 'normal')
        if 'sub_table' in row:
            create_table(row['sub_table']['header'], row['sub_table']['rows'], offset=current_offset+1)

    print_offset(current_offset, max_len+2)
    print_end_section(num_cols=num_field,
                      col_space=max_len+2)
# Справочник аргументов CLI
cli_params_dict = {('-i', '--init'):    {'description':    'Первый запуск',
                                         'import_path':    'modules.init',
                                         'sub_params':     {('id', 'init_dir_path'):               {'description': 'Путь до файлов сонфигураций',
                                                                                                    'default':     './default/'}
                                                            },
                                         'options':        {}
                                         },
                   }

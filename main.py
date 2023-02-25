#! ./venv/bin/python3

# общие пакеты
import sys
import json
from importlib import import_module


# TODO Дописать модуль -v i:[web/cli/gui] или view:[web/cli/gui] для отображения в нужных интерфейсах.

def main(cli_params):

    # Чтение параметров из консоли
    cli_params_dict = json.load(open('config.json'))['CLI_param']
    cli_params = cli_params[1:]
    for existing_param in cli_params_dict:                  # Проходим по всем доступным параметрам приложения
        for num_param, cli_param in enumerate(cli_params):  # Сравниваем со всеми параметрами из консоли
            if cli_param in existing_param:

                # Получаем существующие ключи параметров и значения по умолчанию для модуля из конфига
                modul_args = {existing_sub_param_key: existing_sub_param_d_value['default'] for existing_sub_param_key, existing_sub_param_d_value in cli_params_dict[existing_param]['sub_params'].items()}

                # заменяем параметры по умолчанию на аргументы из консоли для модуля (если такие есть)
                for param in cli_params:
                    cli_param = param.split(':')
                    if cli_param[0] in modul_args:
                        modul_args[cli_param[0]] = cli_param[1]

                module = import_module(cli_params_dict[existing_param]['import_path'])   # Подключаем необходимый модуль
                module.run(modul_args, cli_param)                                        # Запускаем модуль


if __name__ == '__main__':
    main(cli_params=sys.argv)

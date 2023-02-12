import json
import os

def run(argv, main_cli_param):
    config_data = json.load(fp=open('config.json', encoding='utf-8'))
    config_data['main_config']['prj_dir_path'] = os.path.abspath('')
    json.dump(fp=open('config.json', 'w', encoding='utf-8'), obj=config_data, ensure_ascii=False)

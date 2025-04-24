import ipaddress
import json
from typing import MutableMapping
import os
import pyexcel as pe
import importlib
import inspect
from loguru import logger
from pathlib import Path

temp_file = 'out/out.json'
excel_file = 'out/out.xlsx'
Path('out').mkdir(exist_ok=True)

try:
    os.remove(temp_file)
except FileNotFoundError:
    pass

def store_data(host_data, lock):
    with lock:
        if not os.path.exists(temp_file):
            with open(temp_file, 'w') as f:
                json.dump(list(), f)
        try:
            with open(temp_file, 'r') as f:
                data = json.load(f)
            with open(temp_file, 'w') as f:
                if host_data['SSH']['state'] != 'unreachable':
                    data.append(host_data)
                json.dump(data, f, ensure_ascii=False, indent=3)
        except Exception as e:
            log(f'Error while store data: {host_data}/nErros message: {e}')

def load_data():
    with open(temp_file, 'r') as f:
        return json.load(f)

def report():
    new_data = list()
    for item in load_data():
        new_data.append(flatten(item))
    to_excel(new_data)

def to_excel(data):
    pe.save_as(records=data, dest_file_name=excel_file)

def get_ips_from_subnet(subnet_str):
    try:
        network = ipaddress.ip_network(subnet_str, strict=False)
        return [str(ip) for ip in network.hosts()]
    except ValueError as e:
        log(f"Invalid subnet: {e}")
        return []


def log(message):
    logger.debug(message)


def flatten(dictionary, parent_key='', separator='_'):
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten(value, new_key, separator=separator).items())
        else:
            items.append((new_key, value))
    return dict(items)


def import_classes_from_folder(folder_path):
    class_list = []
    folder_path = Path(folder_path)

    # Add folder to Python path temporarily
    import sys
    # sys.path.insert(0, str(folder_path.parent))
    # print(folder_path.absolute())
    try:
        for file_path in folder_path.glob('*.py'):
            module_name = file_path.stem
            module = importlib.import_module(f"{folder_path.name}.{module_name}")
            for _, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and
                        obj.__module__ == f"{folder_path.name}.{module_name}"):
                    class_list.append(obj)

    finally:
        # Remove the temporary path addition
        # sys.path.pop(0)
        pass

    return class_list
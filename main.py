import paramiko
import settings
import multiprocessing
from queue import Empty
from base_check import UnsuccessfulModuleExecution
from misc import *


external_checks = import_classes_from_folder('external_checks')
internal_checks = import_classes_from_folder('internal_checks')
postprocess_modules = import_classes_from_folder('postprocess')

def main():
    with multiprocessing.Pool(processes=settings.process_pool_size) as pool:
        manager = multiprocessing.Manager()
        global_lock = manager.Lock()
        task_queue = manager.Queue(maxsize=1)
        feeder = multiprocessing.Process(target=create_initial_data_and_put_in_queue, args=[task_queue])
        feeder.start()
        count = 0
        try:
            while True:
                try:
                    task = task_queue.get(block=True, timeout=5)
                    pool.apply_async(
                        run_check_tests,
                        args=(task, global_lock),
                    )
                    count += 1
                except Empty:
                    logger.debug('queue is empty, stop task creation')
                    break
        except KeyboardInterrupt:
            print("\nShutting down gracefully...")
        finally:
            logger.debug(f'{count} tasks have been load in pool')
            feeder.terminate()
            pool.close()
            pool.join()
            report()

def create_initial_data_and_put_in_queue(task_queue):
    count = 0
    for group_name in settings.inventory.keys():
        for network_name in settings.inventory[group_name]:
            ip_list = get_ips_from_subnet(settings.inventory[group_name][network_name])
            for ip in ip_list:
                host_data = {
                    'group_name': group_name,
                    'network_name': network_name,
                    'ip': ip
                }
                task_queue.put(host_data, block=True, timeout=0.1)
                count += 1
    logger.debug(f'{count} tasks have been generated')

def run_check_tests(host_data: dict, lock):
    try:
        external_check(host_data)
        internal_check(host_data)
        postprocess(host_data)
    except UnsuccessfulModuleExecution as e:
        logger.debug(e)
    finally:
        logger.debug(host_data)
        store_data(host_data, lock)

def external_check(host_data: dict):
    for module in external_checks:
        module(host_data).check()

def internal_check(host_data: dict):
    for module in internal_checks:
        ssh_client = connect(host_data['ip'])
        if isinstance(ssh_client, paramiko.SSHClient):
            host_data.update({'SSH client': {'error_message': ''}})
            module(host_data, ssh_client).check()
        else:
            host_data.update({'SSH client': {'error_message': ssh_client}})
            return False
    return True

def postprocess(host_data: dict):
    for module in postprocess_modules:
        module(host_data).check()

def connect(host):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for port in settings.ssh_ports:
        try:
            client.connect(hostname=host, username=settings.login_username, port=port)
            return client
        except Exception as e:
            logger.debug(f'Error connecting to host: {str(e)}')
            return str(e)

if __name__ == '__main__':
    main()


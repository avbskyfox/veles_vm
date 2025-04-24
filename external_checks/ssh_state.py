from base_check import BaseExternalCheck, UnsuccessfulModuleExecution
import nmap

class SSHState(BaseExternalCheck):
    name = "SSH"

    def check(self):
        data = self.__nmap_scan(self.host_data['ip'])
        self.host_data.update({self.name: data})
        if data['state'] == 'unreachable':
            raise UnsuccessfulModuleExecution

    @staticmethod
    def __nmap_scan(target, ports='22', arguments='-sV'):
        scanner = nmap.PortScanner()
        scanner.scan(hosts=target, ports=ports, arguments=arguments)
        if target not in scanner.all_hosts():
            return {'state': 'unreachable'}
        return {
            'state': scanner[target].state(),
            'version': scanner[target]['tcp'][22]['product'] + scanner[target]['tcp'][22]['version']
        }

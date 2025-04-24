from base_check import BaseInternalCheck


class FstabHome(BaseInternalCheck):
    name = 'FstabHome'
    etalon = 'defaults,secdel=2'
    host_command = 'cat /etc/fstab|grep /home/'

    def process_data(self) -> bool:
        return self.contain_string()
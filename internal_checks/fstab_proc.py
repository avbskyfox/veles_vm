from base_check import BaseInternalCheck


class FstabProc(BaseInternalCheck):
    name = 'FstabProc'
    etalon = 'proc /proc proc defaults,hidepid=2 0 0'
    host_command = 'cat /etc/fstab|grep proc'

    def process_data(self):
        return self.contain_string()
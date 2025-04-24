from base_check import BaseInternalCheck


class MacLevels(BaseInternalCheck):
    name = 'MacLevels'
    etalon = '''НС:0
ДСП:1
С:2
СС:3'''
    host_command = 'cat /etc/parsec/mac_levels'

    def process_data(self):
        return self.contain_string()
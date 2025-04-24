from base_check import BaseInternalCheck


class NoChmodX(BaseInternalCheck):
    name = 'NoChmodX'
    etalon = '1'
    host_command = 'cat /parsecfs/nochmodx'

    def process_data(self):
        return self.strict_equal()
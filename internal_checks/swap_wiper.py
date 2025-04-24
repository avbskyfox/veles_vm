from base_check import BaseInternalCheck


class SwapWiper(BaseInternalCheck):
    name = 'SwapWiper'
    etalon = 'ENABLED=Y'
    host_command = 'cat /etc/parsec/swap_wiper.conf|grep ENABLED='

    def process_data(self):
        return self.strict_equal()
from base_check import BaseInternalCheck


class DigSig(BaseInternalCheck):
    name = 'DigSig'
    etalon = 'АКТИВНО'
    host_command = 'sudo astra-digsig-control status'

    def process_data(self) -> bool:
        return self.strict_equal()
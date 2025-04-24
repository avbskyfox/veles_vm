from base_check import BaseInternalCheck


class PasswordLength(BaseInternalCheck):
    name = 'PasswordLength'
    etalon = 'pam_cracklib.so retry=3 difok=3 enforce_for_root minlen=8 lcredit=-1 ucredit=-1 dcredit=-1 ocredit=0'
    host_command = 'cat /etc/pam.d/common-password|grep pam_cracklib.so'

    def process_data(self) -> bool:
        return self.contain_string()
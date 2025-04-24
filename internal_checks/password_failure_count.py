from base_check import BaseInternalCheck


class CommonAuthCheck(BaseInternalCheck):
    name = 'CommonAuth'
    etalon = 'pam_tally.so per_user deny=3 lock_time=10 unlock_time=10'
    host_command = 'cat /etc/pam.d/common-auth|grep pam_tally.so'

    def process_data(self) -> bool:
        return self.contain_string()
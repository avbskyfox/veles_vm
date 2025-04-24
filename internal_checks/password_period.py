from base_check import BaseInternalCheck


class PasswordPeriod(BaseInternalCheck):
    name = 'PasswordPeriod'
    etalon = '''PASS_MAX_DAYS 90
PASS_MIN_DAYS 45
PASS_WARN_AGE 14
'''
    host_command = 'cat /etc/login.defs|grep PASS_MAX_DAYS && cat /etc/login.defs|grep PASS_MIN_DAYS && cat /etc/login.defs|grep PASS_WARN_AGE '

    def process_data(self) -> bool:
        return self.contain_string()
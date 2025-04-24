from base_check import BaseInternalCheck


class Uname(BaseInternalCheck):
    name = 'linux_kernel_version'
    etalon = '5.4.0-162-hardened'
    host_command = 'uname -a'

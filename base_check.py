import paramiko


class BaseCheck:
    """
    Base class for all checks
    """
    def __init__(self, host_data: dict):
        """
        :param host_data: it contains all host data to use it in check and enrich it with new data after check
        """
        self.host_data = host_data

    name = "Base check"

    def check(self):
        """
        Enrich host data with result of check
        :return: None
        """

class UnsuccessfulModuleExecution(Exception):
    pass


class BaseExternalCheck(BaseCheck):
    """
    Base class for all external checks for porpoises like ports scans
    """
    name = "Base external checks"


class BaseInternalCheck(BaseCheck):
    """
    Base class for internal checks by SSH
    """
    def __init__(self, host_data: dict, client: paramiko.client.SSHClient):
        super().__init__(host_data)
        self.client = client

    name = "Base internal checks"
    result = None
    host_command = None
    etalon = None
    fact = None

    def check(self):
        self.__invoke_host_data()
        self.__invoke_process_data()
        new_data = {
            self.name: {
                'host_command': self.host_command,
                'etalon': self.etalon,
                'fact': self.fact,
                'result': self.result
            }
        }
        self.host_data.update(new_data)

    def get_data(self) -> str:
        stdin, stdout, stderr = self.client.exec_command(self.host_command)
        return_data = stdout.read().decode() + stderr.read().decode()
        return  return_data.rstrip()

    def process_data(self) -> bool:
        return self.contain_string()

    def contain_string(self):
        return True if self.fact.find(self.etalon) >= 0 else False

    def strict_equal(self):
        return True if self.fact == self.etalon else False

    def __invoke_host_data(self):
        self.fact = self.get_data()

    def __invoke_process_data(self):
        self.result = self.process_data()
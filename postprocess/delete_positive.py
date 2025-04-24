from base_check import BaseCheck

class DeletePositive(BaseCheck):
    def check(self):
        new_host_data = self.host_data.copy()
        for key, value in new_host_data.items():
            try:
                if value['result']:
                    self.host_data.pop(key)
            except KeyError:
                pass

from base_check import BaseCheck

class DeletePositive(BaseCheck):
    def check(self):
        new_host_data = {}
        for key, value in self.host_data.items():
            try:
                if not value['result']:
                    new_host_data.update({key, value})
            except KeyError:
                new_host_data.update({key, value})
        self.host_data = new_host_data
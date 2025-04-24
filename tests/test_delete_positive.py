from unittest import TestCase

from main import external_checks
from postprocess.delete_positive import DeletePositive

class TestDeletePositive(TestCase):
    def test_check(self):
        host_data = {
            'check1': {'result': True},
            'check2': {'result': False}
        }
        obj = DeletePositive(host_data)
        obj.check()
        try:
            print(host_data['check1'])
        except KeyError:
            pass
        else:
            self.fail('True checks was not deleted')

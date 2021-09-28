import os
import pytest


cur_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(cur_dir, 'conf/test.yaml')


@pytest.fixture(scope='session')
def port():
    return 8090

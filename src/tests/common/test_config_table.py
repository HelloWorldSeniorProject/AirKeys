from common.config_table import ConfigTable
from common.types import *


def test_ct = ConfigTable()

print(ct)

ct.set_state(SystemState.Inactive)

print(ct)

ct2 = ConfigTable()

print(ct2)

print(ct is ct2)
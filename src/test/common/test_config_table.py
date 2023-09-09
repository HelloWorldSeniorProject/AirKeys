from common.config.config_table import ConfigTable
from common.types import *
from test.swte import large_banner, small_banner


class Test_ConfigTable:
    def test_singleton(self):
        large_banner(
            "Test Config Table Singleton: Tests Config Table's Singleton inheritence"
        )

        ct1 = ConfigTable()
        ct2 = ConfigTable()
        assert ct1 is ct2

        ct3 = ConfigTable()
        assert ct1 is ct2 is ct3

    def test_setup(self):
        large_banner(
            "Test Config Table: Tests Config Tables's instantiation instantiation logic"
        )

        ct = ConfigTable()
        small_banner(f"Config Table vars:\n\t{ct.vars()}")

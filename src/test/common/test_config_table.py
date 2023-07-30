from common.config_table import ConfigTable
from common.types import *
from test.swte import large_banner, small_banner


def test_config_table():
    large_banner("Test Config Table: Tests Config Tables's instantiation instantiation logic")
    
    ct= ConfigTable()
    assert( ct.get_state() == SystemState.Standby )
    
def test_config_table_singleton():
    large_banner("Test Config Table Singleton: Tests Config Table's Singleton inheritence")
    
    
    ct1= ConfigTable()
    ct2 = ConfigTable()
    assert(ct1 is ct2)
    
    ct3 = ConfigTable()
    assert(ct1 is ct2 is ct3)
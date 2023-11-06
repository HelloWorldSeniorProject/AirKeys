from common.config.config_table import ConfigTable
from common.types import *
from test.swte import *


class Test_ConfigTable:
    @requirements(3.1)
    def test_singleton(self):
        large_banner("Test Singleton: Tests singleton inheritence")

        small_banner("Instantiate multiple Config Tables.")

        cts = []

        # verify multiple inits point to the same object.
        cts.append(ConfigTable())
        cts.append(ConfigTable())

        # change values and verify again.
        cts[0].set_mode(Mode.Active)
        config_dict = cts[0].to_dictionary()
        temp = ConfigTable()
        temp.write(config_dict)
        cts.append(temp)

        exps_met = []

        small_banner("Verify each CT points to the same object")

        for i, ct in enumerate(cts[1:]):
            exps_met.append(ct is cts[i - 1])
        assert all(exps_met)

    def test_setup(self):
        large_banner("Test Setup: Tests instantiation logic")

        # get defaults as defined in class.
        defaults = vars(ConfigTable)["_DEFAULTS"]

        small_banner("Verify class data matches expected defaults")
        ct = ConfigTable()

        exps_met = []

        # compare defaults to actual variables inside config table class (i.e. self._var).
        for act, exp in zip(vars(ct).values(), defaults.values()):
            exps_met.append(act == exp)

        assert all(exps_met)

    @requirements(3.2)
    def test_write(self):
        large_banner("Test Write: Tests classes ability to set all instance variables.")

        CFG_DATA = [
            {
                "mode": Mode.Standby,
                "layout": "Qwerty",
                "connection": Connection.UsbA,
                "device": Device.Large,
                "os": OperatingSystem.Windows,
            },
            {
                "mode": Mode.Inactive,
                "layout": "Qwerty",
                "connection": Connection.UsbA,
                "device": Device.Large,
                "os": OperatingSystem.Mac,
            },
            {
                "mode": Mode.Standby,
                "layout": "Qwerty",
                "connection": None,
                "device": Device.Small,
                "os": OperatingSystem.Windows,
            },
            {
                "mode": Mode.Standby,
                "layout": "Azerty",
                "connection": Connection.UsbC,
                "device": Device.Large,
                "os": OperatingSystem.Linux,
            },
            {
                "mode": Mode.Active,
                "layout": "Qwerty",
                "connection": Connection.Bluetooth,
                "device": Device.Large,
                "os": OperatingSystem.Windows,
            },
        ]

        ct = ConfigTable()
        small_banner("Verify instance variables are set as expected.")

        exps_met = []
        for cfg in CFG_DATA:
            # write new config data
            ct.write(cfg)

            # compare each var
            for act, exp in zip(vars(ct).values(), cfg.values()):
                exps_met.append(act == exp)

        assert all(exps_met)

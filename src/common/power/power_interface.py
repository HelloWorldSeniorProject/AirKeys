import subprocess

from common.config.config_table import ConfigTable
from util.logger import get_logger
from common.file.file_manager import FileManager

logger = get_logger("PowerInterface.log", overwrite=False)


class PowerInterface:
    # TODO : implement
    @staticmethod
    def sleep():
        pass

    # TODO : determine if cameras need to be shutdown.
    @staticmethod
    def power_off():
        """Powers off device.

        Note:
            Saves latest config table information to file before powering off. Does not confirm choice!
            Use with caution.
        """

        logger.warn("Preparing to shutdown device.")

        # save config table to file.
        cfg = ConfigTable()
        file_mgr = FileManager()
        if not (file_mgr.write_configuration_file(config=cfg.to_dictionary())):
            logger.error("Failed to save latest configuration.")
        else:
            logger.info("Saved latest configuration to file.")

        logger.info("Powering off.")

        cmd = ["shutdown", "-h", "now"]  # os command  # power off system  # immediately
        subprocess.run(cmd)

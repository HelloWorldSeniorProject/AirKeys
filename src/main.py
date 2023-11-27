# Python
import sys
from threading import Thread
from multiprocessing import Process, Manager


# AirKeys Interfaces
from common.config.config_table import ConfigTable
from common.file.file_manager import FileManager
from common.power.power_interface import PowerInterface
from common.time.internal_clock import InternalClock

# AirKeys Utils
from util.logger import get_logger

logger = get_logger("Main.log")

""" Main program thread. Functions as object Factory & Controller """

# TODO : finish


def main():
    # initialize system resources
    try:
        clock = InternalClock()
        ct = ConfigTable()
        fm = FileManager()

        # try to load previous config table
        ct.write(fm.read_configuration_file())
    except Exception as e:
        exit_with_failure(f"Failed to initialize system resources.\n{e}")

    # TODO set threads to begin running setup
    while True:
        continue

    # Finish current task
    PowerInterface.power_off()


def exit_with_failure(message: str):
    """Exits the program with failure status.

    Args:
        message : the message to display in logs upon failure.
    Note:
        Does not power off system, only exits the main program.
    """
    logger.error(message)
    sys.exit(1)


# run program
if __name__ == "__main__":
    main()

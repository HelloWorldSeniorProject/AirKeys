# Python
import sys



# AirKeys Interfaces
from common.config.config_table import ConfigTable
from common.file.file_manager import FileManager
from common.power.power_interface import PowerInterface
from common.time.internal_clock import InternalClock
from data.stream import DataStream
from common.types import *

# AirKeys Utils
from util.logger import get_logger

# Standard Modules
import multiprocessing

logger = get_logger("Main.log")

""" Main process. Functions as object Factory & Controller"""


def main():
    """Initializes all system resources and executes main program loop.
    """

    # any failure here is critical. Exit program if so.
    try:
        logger.info("Initializing System Resources.")
        clock = InternalClock() 
        ct = ConfigTable()
        fm = FileManager()
        stream = DataStream()
        # TODO: add data processing interface
        # processor = DataProcessor()
        # TODO add connection manager interface

        logger.info("Initialization Complete")
        
        # try to load previous config table and set to calibration mode.
        prev_config = fm.read_configuration_file()
        if prev_config == None:
            logger.info("No previous configuration detected.")
        else:
            ct.write(prev_config=prev_config)

        # TODO: attempt to connect to external device
        logger.info(f"Attempting to connect to external device using {ct.get_connection().value}.")



        # setup input and display layout
        logger.info("Attempting to setup cameras.")
        captures = stream.setup_cameras(num_cameras=2)
        logger.info("Camera setup complete.")
        

        # TODO: Abstract to utility function once done.
        logger.info("Entering calibration mode.")
        ct.set_mode(mode=Mode.Calibration)
        stream.display_frame(frame=fm.get_layout_file(f_name=ct.get_layout()))
        calibration_frames = stream.get_frame_data(captures=captures)
        # processor.detect_keys(calibration_frames)
        ct.set_mode(mode=Mode.Active)
        logger.info("Calibration complete.")
        
    except Exception as e:
        exit_with_failure(f"Failed to initialize system resources.\n{e}")


    while True:
        continue

    # Finish current task
    PowerInterface.power_off()


    ct.set_mode(mode=Mode.Calibration)

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

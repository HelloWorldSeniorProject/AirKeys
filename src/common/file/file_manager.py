import os, sys, json
from common.patterns.singleton import Singleton
from common.util.logger import get_logger
from common.util.info import FILE_DIR
import numpy as np
import cv2

logger = get_logger("FileManager.log")

CONFIG_FNAME = "config.json"


class InvalidFileType(Exception):
    """An exception thrown when attempting to store/retrieve an unknown file type."""

    def __init__(self, f_type: str):
        super().__init__(f"File type {f_type} is not valid.")


class FileManager(metaclass=Singleton):
    """A set of targeted file operations for use across the syste.

    File Manager is a singleton class that has functions for the storage and retrieval of files
    within the system. These operations will be used in most cases of file IO.

    Args:
        _LOCATIONS: a dictionary containing predefined paths for every type of expected data.
    """

    _LOCATIONS = {
        "layout": os.path.join(FILE_DIR, "layouts"),
        "config": os.path.join(FILE_DIR, "config"),
        "calibration": os.path.join(FILE_DIR, "calibration"),
    }

    def __init__(self):
        """Initializes the instance"""
        logger.info("Initializing File Manager.")

        try:
            self._check_file_locations()
        except OSError:
            logger.error("Failed to make one or more necessary file directories.")
            sys.exit(1)

        logger.info("Initialized File Manager successfully.")

    def _check_file_locations(self):
        """Creates necessary file locations if necessary.

        Note:
            Utilizies OS calls; may require elevated permissions.
        """

        logger.info("Checking file locations.")

        try:
            if not (os.path.exists(FILE_DIR)):
                logger.warning(f"File directory '{FILE_DIR}' not found. Creating.. ")
                os.mkdir(FILE_DIR)

            for key, loc in self._LOCATIONS.items():
                if not (os.path.exists(loc)):
                    logger.warning(
                        f"{key.capitalize()} file directory '{loc}' not found. Creating... "
                    )
                    os.mkdir(loc)
        except Exception as e:
            logger.error(f"Failed to make necessary directories.\n{e}")
            raise

    def _create_file(
        self, f_type: str, f_name: str, f_data, overwrite: bool = False
    ) -> bool:
        """Creates a in file and saves in expected location.

        Args:
            f_type : the expected type of file data. Must exactly match a location in _LOCATIONS.
            f_name : the name to save the file as.
            f_data : the data to save to file.
            overwrite: whether to overwrite file if it already exists. Defaults to False.

        Returns:
            True if the operation was a success; false otherwise.
        Note:
            If data is of type Numpy Array, the function will use OpenCV's image write function
            function to create a new image.
        """
        # verify folder of desired file type exists.
        try:
            type_dir = self._LOCATIONS[f_type]
        except:
            raise InvalidFileType(f_type)

        if not (os.path.exists(type_dir)):
            logger.error(f"Expected file directory '{type_dir}' not found.")
            return False

        # verify file doesn't already exist.
        full_file_path = os.path.join(type_dir, f_name)
        if (not overwrite) and (os.path.exists(full_file_path)):
            logger.error(f"Matching filename '{f_name}' found in '{type_dir}'.")
            return False

        # attempt to create file.
        try:
            if type(f_data) == np.array:
                cv2.imwrite(full_file_path, f_data)
            else:
                with open(full_file_path, "w") as file:
                    json.dump(f_data, file, indent=4)
        except OSError:
            logger.error(f"Failed to write to {file}.")
            return False

        logger.info(f"Succesfully create file {file}.")
        return True

    def _retrieve_file(self, f_type: str, f_name: str) -> str:
        """Finds a file in specified location and returns full file path.

        Args:
            f_type : the expected type of file. Must exactly match a location in _LOCATIONS.
            f_name : the name of the file.

        Returns:
            The full path to desired file.
        Note:
            Will return None if file does not exist.
        """

        try:
            search_dir = self._LOCATIONS[f_type]
        except:
            raise InvalidFileType(f_type)

        if not (os.path.exists(search_dir)):
            logger.error(f"Expected file directory '{search_dir}' not found.")
            return None

        full_file_path = os.join(search_dir, f_name)
        if not (os.path.exists(full_file_path)):
            logger.error(f"File '{f_name}' does not exist in '{search_dir}'.")
            return None

        return full_file_path

    def _get_files(self, f_type: str) -> list[str]:
        """Fetches all files within a specified location.

        Args:
            f_type : the file type to search. Must exactly match a location in _LOCATIONS.

        Returns:
            A list of full file paths for every file in location.
        Note:
            Returns None if no files are found in directory.
        """
        try:
            search_dir = self._LOCATIONS[f_type]
        except:
            raise InvalidFileType(f_type)

        if not (os.path.exists(search_dir)):
            logger.error(f"Expected file directory '{search_dir}' not found.")
            return None

        files = []
        for f in os.listdir(search_dir):
            full_path = os.join(search_dir, f)

            if os.path.isfile(full_path):
                files.append(full_path)

        if len(files) == 0:
            logger.warning(f"No files in directory '{search_dir}'.")
            return None

        return files

    def _readImage(self, f_name: str) -> np.array:
        """Fetches data from image file.

        Args:
            f_name : the full file path of the image file.

        Returns:
            Image data as Numpy Array.
        """
        try:
            return cv2.imread(f_name)
        except Exception as e:
            logger.error(f"Failed to read img at '{f_name}'.\n{e}")
            return None

    def get_layout_file(self, f_name: str) -> np.array:
        """Fetches data from specified layout file.

        Args:
            f_name : the name of image file in layouts folder.

        Returns:
            Image data as Numpy Array.
        """

        layout = self._retrieve_file(f_type="layout", f_name=f_name)

        if layout == None:
            logger.error("Failed to find layout file.")
            return None

        return self._readImage(f_name)

    def get_calibration_file(self, f_name):
        """Fetches data from specified calibration file.

        Args:
            f_name : the name of image file in calibration folder.

        Returns:
            Image data as Numpy Array.
        """
        calibration = self._retrieve_file(f_type="calibration", f_name=f_name)

        if calibration == None:
            logger.error("Failed to find layout file.")
            return None

        return self._readImage(f_name)

    def read_configuration_file(self) -> dict:
        """Fetches data from configuration file.

        Returns:
            A dictionary with config table items as keys and their known last values.
        """
        config = self._retrieve_file(f_type="config", f_name=CONFIG_FNAME)

        if config == None:
            logger.warning("No config file found.")
        else:
            with open(config, "r") as f:
                config = json.load(f, object_pairs_hook=dict)

        return config

    # TODO : Figure out how UI may pass data
    def upload_layout(self, f_name: str) -> bool:
        pass

    def upload_calibration(self, f_name: str) -> bool:
        pass

    def write_configuration_file(self, config: dict) -> bool:
        """Saves configuration data to file.

        Args:
            config : a dictionary with config table items as keys and their known last values.

        Returns:
            True if the operation was successful; false otherwise.
        """
        return self._create_file(
            f_type="config", f_name=CONFIG_FNAME, f_data=config, overwrite=True
        )

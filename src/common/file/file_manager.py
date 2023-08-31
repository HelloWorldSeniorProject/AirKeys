import os, sys
from common.patterns.singleton import Singleton
from common.util.logger import get_logger
from common.util.info import FILE_DIR
from collections import OrderedDict
import cv2


logger = get_logger("FileManager.log")

class InvalidFileType(Exception):
    
    def __init__(self, f_type:str):
        super().__init__(f"File type {f_type} is not valid.")
        

class FileManager(metaclass=Singleton):

    LOCATIONS = {
        "layout": os.path.join(FILE_DIR, "layouts"),
        "config": os.path.join(FILE_DIR, "config"),
        "calibration": os.path.join(FILE_DIR, "calibration"),
    }

    def __init__(self):
        logger.info("Initializing File Manager.")
        
        try:
            self._check_file_locations()
        except OSError:
            logger.error("Failed to make one or more necessary file directories.")
            sys.exit(1)
            
        logger.info("Initialized File Manager successfully.")
            
        

    def _check_file_locations(self):
        
        logger.info("Checking file locations.")
        
        if not(os.path.exists(FILE_DIR)):
            logger.warning(f"File directory '{FILE_DIR}' not found. Creating.. ")
            os.makedir(FILE_DIR)
            
        for key, loc in self.LOCATIONS.items():
            if not(os.path.exists(loc)):
                logger.warning(f"{key.capitalize()} file directory '{loc}' not found. Creating... ")
                os.makedir(loc)
                
    def _create_file(self, f_type:str, f_name:str, f_data) -> bool:
        
        try:
            type_dir = self.LOCATIONS[f_type]
        except:
            raise InvalidFileType(f_type)
        
        if not(os.path.exists(type_dir)):
            logger.error(f"Expected file directory '{type_dir}' not found.")
            return False
        
        try:
            with open(os.path.join(type_dir, f_name), 'w') as file:
                file.write(f_data)
        except OSError:
            logger.error(f"Failed to write to {file}.")
            return False
        
        logger.info(f"Succesfully create file {file}.")
        return True 
            
    
    def _retrieve_file(self, f_type:str, f_name:str) -> str:
        
        try:
            search_dir = self.LOCATIONS[f_type]
        except:
            raise InvalidFileType(f_type)
        
        if not(os.path.exists(search_dir)):
            logger.error(f"Expected file directory '{search_dir}' not found.")
            return None
        
        full_file_path = os.join(search_dir, f_name)
        if not(os.path.exists(full_file_path)):
            logger.error(f"File '{f_name}' does not exist in '{search_dir}'.")
            return None
        
        return full_file_path
        
        
    def _get_files(self, f_type:str) -> list[str]:
        try:
            search_dir = self.LOCATIONS[f_type]
        except:
            raise InvalidFileType(f_type)
        
        if not(os.path.exists(search_dir)):
            logger.error(f"Expected file directory '{search_dir}' not found.")
            return None
        
        files = []
        for f in os.listdir(search_dir):
            full_path = os.join(search_dir, f)
            
            if os.path.isfile(full_path):
                files.append(full_path)
                
        if (len(files) == 0):
            logger.warning(f"No files in directory '{search_dir}'.")
            return None
        
        return files
    
    def _readImage(self, f_name:str):
        try:
            return cv2.imread(f_name)
        except Exception as e:
            logger.error(f"Failed to read img at '{f_name}'.\n{e}")
            return None
    
    def get_layout_file(self, f_name:str):
        layout = self._retrieve_file(f_type="layout", f_name=f_name)
        
        if layout == None:
            logger.error("Failed to find layout file.")
            return None
        
        return self._readImage(f_name)
        

    # TODO : implement
    def get_calibration_file(self, f_name):
        pass
    # TODO : implement 
    def read_configuration_file(self, f_name) -> OrderedDict:
        pass
    
    
        
    # TODO : Figure out how UI may pass data
    def upload_layout(self, f_name:str):
        pass
    
    
        
            
        
        
        
                

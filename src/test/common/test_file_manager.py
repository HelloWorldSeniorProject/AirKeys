import os, shutil
from common.file.file_manager import FileManager, FILE_DIR
from common.types import *
from test.swte import large_banner
from pytest import fail
    
class Test_FileManager:
    
    def test_singleton():
        large_banner(
            "Test File Manager Singleton: Tests File Manager's singleton inheritence"
        )

        fm1 = FileManager()
        fm2 = FileManager()
        assert fm1 is fm2

        fm3 = FileManager()
        assert fm1 is fm2 is fm3
        
    def test_setup():
        large_banner(
            "Test File Manager Setup: Test File Manager's instantiation and folder creation"
        )
        
        # delete existing folders if they exist
        if os.path.exists(FILE_DIR):
            try:
                shutil.rmtree(FILE_DIR)
            except:
                fail(f"Failed to remove '{FILE_DIR}' from codebase.")
        
        # verify folder creation after instantiation
        fm = FileManager()
        locations = [FILE_DIR] + [loc for loc in fm._LOCATIONS.values()]
        exps_met = []
        for loc in locations:
            exps_met.append(os.path.exists(loc))

        assert(all(exps_met))

    def test_read_file():
        pass

            

        
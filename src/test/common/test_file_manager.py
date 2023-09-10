import os, shutil, json, requests
import numpy as np, cv2
from pytest import fail
from common.file.file_manager import FileManager, FILE_DIR
from common.types import *
from test.swte import large_banner, small_banner


class Test_FileManager:
    def test_singleton(self):
        large_banner("Test Singleton: Tests singleton inheritence.")

        small_banner("Instantiate multiple File Managers.")

        fms = []

        # verify multiple inits point to the same object.
        fms.append(FileManager())
        fms.append(FileManager())

        exps_met = []

        small_banner("Verify each FM points to the same object")

        for i, fm in enumerate(fms[1:]):
            exps_met.append(fm is fms[i - 1])

        assert all(exps_met)

    def test_setup(self):
        large_banner("Test Setup: Test instantiation and folder creation.")

        print(FILE_DIR)

        # delete existing folders if they exist
        if os.path.exists(FILE_DIR):
            try:
                shutil.rmtree(FILE_DIR)
            except:
                fail(f"Failed to remove '{FILE_DIR}' from codebase.")

        small_banner("Verify folder creation after instantiation")

        # get base location plus every location defined in class.
        locations = [FILE_DIR] + [
            loc for loc in vars(FileManager)["_LOCATIONS"].values()
        ]

        # we only need the instantiation logic to run, not any of the class data.
        FileManager()
        exps_met = []
        for loc in locations:
            exps_met.append(os.path.exists(loc))

        assert all(exps_met)

    def test_read_file(self):
        large_banner("Test Read File: Tests the file reading logic ")
        # create fake image
        pass

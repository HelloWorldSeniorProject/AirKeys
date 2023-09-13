import os, shutil, json, requests
import numpy as np, cv2, pytest
from common.file.file_manager import FileManager, FILE_DIR, InvalidFileType
from common.types import *
from test.swte import *


class Test_FileManager:
    def _download_temp_images(self) -> dict:
        # source: https://picsum.photos/
        TEST_IMAGES = {
            "img0": "https://picsum.photos/seed/picsum/200/300",
            "img1": "https://picsum.photos/200/300?grayscale",
            "img2": "https://picsum.photos/200/300",
        }

        small_banner("Create temp images folder.")

        imgs_f = os.path.join(TEMP_DIR, "images")
        try:
            if not os.path.exists(imgs_f):
                os.mkdir(imgs_f)
        except Exception as e:
            pytest.fail(f"Failed to make images folder at '{imgs_f}'\n{e}")

        small_banner("Download test images.")
        for img in TEST_IMAGES.keys():
            url = TEST_IMAGES[img]

            # send request to site
            res = requests.get(url, stream=True)
            if res.status_code != 200:
                pytest.fail(f"Failed to fetch picture at {url}")

            # store image in temp folder
            img_f = os.path.join(imgs_f, f"{img}.png")

            with open(img_f, "wb") as f:
                shutil.copyfileobj(res.raw, f)

        return TEST_IMAGES

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

    @conditional
    # Reason : Removes folders that may contain non-trivial data.
    def test_setup(self):
        large_banner("Test Setup: Test instantiation and folder creation.")

        print(FILE_DIR)

        # delete existing folders if they exist
        if os.path.exists(FILE_DIR):
            try:
                shutil.rmtree(FILE_DIR)
            except:
                pytest.fail(f"Failed to remove '{FILE_DIR}' from codebase.")

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

    @conditional
    # Verify by inspection. Will not work in dev env as there is no display.
    def test_read_image(self):
        large_banner("Test Read File: Tests the file reading logic ")

        fm = FileManager()

        TEST_IMAGES = self._download_temp_images()

        for img in TEST_IMAGES.keys():
            url = TEST_IMAGES[img]
            small_banner(f"Showing '{img}', compare to img at '{url}'.")
            small_banner(f"Press any button in window to close.")

            img_f = os.path.join(TEMP_DIR, "images", f"{img}.png")

            img_data = fm._read_image(img_f)
            cv2.imshow("Test Image", img_data)

            cv2.waitKey(0)

    def test_retrieve_file(self):
        large_banner(
            "Test Retrieve File: Tests file retrieval logic and error handling"
        )
        
        fm = FileManager()
        exps_met = []

        # [ {"key0" : 0}, {"key1" : 1}, ... ]
        TEST_JSON = {}

        for i in range(32):
            TEST_JSON[f"key{i}"] = i

        small_banner("Generate test file")
        file = os.path.join(FILE_DIR, "calibration", "test.json")

        try:
            with open(file, "w") as f:
                json.dump(TEST_JSON, f)
        except Exception as e:
            pytest.fail(f"Failed write to file '{file}'.\n{e}")
            

        small_banner("Verify file found")
        exps_met.append(fm._retrieve_file("calibration", "test.json") == file)
        # delete test file
        try:
            os.remove(file)
        except Exception as e:
            # should not affect test's acceptance
            logger.warn(f"Failed to delete file '{file}'.\n{e}")
            
        small_banner("Verify 'None' is returned when matching file doesn't exist.")
        exps_met.append(fm._retrieve_file("calibration", "test.json") == None)

        small_banner("Verify file type is enforced")
        try:
            fm._retrieve_file("fubar", "test.json")
        except InvalidFileType:  # expected exception
            small_banner("Failed as expected")
        except Exception as e:  # all others
            pytest.fail(f"Did not throw expected exception\n{e}")
            

        assert all(exps_met)
        
        

    def test_create_file(self):
        large_banner("Test Create File: Tests file creation logic and error handling")

        fm = FileManager()
        exps_met = []

        # [ {"key0" : 0}, {"key1" : 1}, ... ]
        TEST_JSON = {}

        for i in range(32):
            TEST_JSON[f"key{i}"] = i

        small_banner("Generate JSON and verify read data matches.")
        exps_met.append(fm._create_file("calibration", "test.json", TEST_JSON))

        file = os.path.join(FILE_DIR, "calibration", "test.json")

        try:
            with open(file, "r") as f:
                data = json.load(f)
        except Exception as e:
            pytest.fail(f"Failed to open file '{file}'.\n{e}")
            
        exps_met.append(data == TEST_JSON)

        small_banner("Verify overwrite functionality")
        # file already exists; should return false.
        exps_met.append(fm._create_file("calibration", "test.json", TEST_JSON) == False)

        # ignore file already existing; should return true.
        exps_met.append(
            fm._create_file("calibration", "test.json", TEST_JSON, overwrite=True)
            == True
        )

        # delete test file
        try:
            os.remove(file)
        except Exception as e:
            # should not affect test's acceptance
            logger.warn(f"Failed to delete file '{file}'.\n{e}")

        small_banner("Verify file type is enforced")
        try:
            fm._create_file("fubar", "test.json", TEST_JSON)
        except InvalidFileType:  # expected exception
            small_banner("Failed as expected")
        except Exception as e:  # all others
            pytest.fail(f"Did not throw expected exception\n{e}")

        assert all(exps_met)

    def test_get_files(self):
        large_banner("Test Get Files: Tests file gathering logic and error handling")

        exps_met = []
        fm = FileManager()

        # simple util
        def full_path(f):
            return os.path.join(FILE_DIR, "config", f)

        TEST_FILES = []

        # [ {FILEDIR}/config/test0.txt, {FILEDIR}/config/test1.txt]
        for i in range(10):
            TEST_FILES.append(full_path(f"test{i}.txt"))

        small_banner("Create test files.")
        for file in TEST_FILES:
            if os.path.exists(file):
                small_banner(f"Skipping file '{file}'. Already exists.")
                TEST_FILES.remove(file)
                continue

            with open(file, "w") as f:
                f.write("This is a test file")

        small_banner("Verify all created files found.")
        found = fm._get_files("config")
        for file in TEST_FILES:
            # ensure file exists
            if not os.path.exists(file):
                pytest.fail(f"File '{file}' does not exist.")

            exps_met.append(file in found)

            # delete file
            try:
                os.remove(file)
            except Exception as e:
                # should not affect test's acceptance.
                logger.warn(f"Failed to remove file '{file}'\n{e}")

        small_banner("Verify file type is enforced.")
        try:
            fm._get_files("fubar")
        except InvalidFileType:  # expected exception
            small_banner("Failed as expected")
        except Exception as e:  # all others
            pytest.fail(f"Did not throw expected exception\n{e}")

        assert all(exps_met)

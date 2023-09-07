import os

# define directories as a constants.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
DOCS_DIR = os.path.join(ROOT_DIR, "documentation")
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
SRC_DIR = os.path.join(ROOT_DIR, "src")
SCRIPT_DIR = os.path.join(ROOT_DIR, "scripts")
FILE_DIR = os.path.join(ROOT_DIR, "files")
TEST_DIR = os.path.join(SRC_DIR, "test")

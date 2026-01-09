"""Configuration constants for the todo application."""

import os

DEFAULT_SECTION = "GENERAL"
EMPTY_DATE = ""

# File paths
DIR_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_FILE_PATH = os.path.join(DIR_PATH, "data.json")

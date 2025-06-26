import pathlib

SRC_PATH = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = SRC_PATH.parent.parent
PRESET_SAVE_PATH = PROJECT_ROOT / "data" / "presets"

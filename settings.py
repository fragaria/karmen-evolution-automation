import logging

logger = logging.getLogger('settings')


SLICER_APP_EXECUTABLE='/path/to/PrusaSlicerApplication'
SLICER_CONFIG_FILE='config.ini'
KARMEN_API_KEY='YOU CAN CREATE API KEY IN KARMEN'
KARMEN_GROUP_ID='YOUR GROUP ID FROM KARMEN'

KARMEN_API_URL='https://backend.next.karmen.tech/api/2'

SLICER_CONFIG_FILE='my-prusaslicer-config.ini'
GCODE_OUTPUT_FILE='my-tmp-gcode-file.gcode'


_DEFAULT_KARMEN_API_KEY=KARMEN_API_KEY
_DEFAULT_KARMEN_GROUP_ID=KARMEN_GROUP_ID
_DEFAULT_SLICER_CONFIG_FILE=SLICER_CONFIG_FILE
_DEFAULT_GCODE_OUTPUT_FILE=GCODE_OUTPUT_FILE
_DEFAULT_SLICER_APP_EXECUTABLE=SLICER_APP_EXECUTABLE

try:
    from local_settings import *
except ImportError:
    logger.warning('There is no local_settings module. If you want to modify'
        'settings, create local_settings.py file instead of modifying'
        'project default setting.py.')
    pass
assert _DEFAULT_KARMEN_API_KEY != KARMEN_API_KEY, 'You need to change API key (KARMEN_API_KEY).'
assert _DEFAULT_KARMEN_GROUP_ID != KARMEN_GROUP_ID, 'You need to change Karmen group ID (KARMEN_GROUP_ID).'
assert _DEFAULT_SLICER_CONFIG_FILE != SLICER_CONFIG_FILE, 'You need to change PrusaSlicer config file (SLICER_CONFIG_FILE).'
assert _DEFAULT_GCODE_OUTPUT_FILE != GCODE_OUTPUT_FILE, 'You need to change Gcode output file (GCODE_OUTPUT_FILE).'
assert _DEFAULT_SLICER_APP_EXECUTABLE != SLICER_APP_EXECUTABLE, 'You need to change path to PrusaSlicer application (SLICER_APP_EXECUTABLE).'

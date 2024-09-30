import sys
import os.path
import subprocess
import requests

from settings import KARMEN_API_KEY, KARMEN_GROUP_ID, KARMEN_API_URL, \
    SLICER_APP_EXECUTABLE, SLICER_CONFIG_FILE, GCODE_OUTPUT_FILE


def on_error(msg):
    print_msg(f'ERROR: {msg}')
    sys.exit()


def print_msg(msg):
    print(f'\n\033[1m{msg}\033[0m')


# check input file exists
if sys.argv and len(sys.argv) > 1 and sys.argv[1]:
    inputfile = str(sys.argv[1])
else:
    on_error(f'Please provide path to your STL file.')
if not os.path.isfile(inputfile):
    on_error(f'STL file {inputfile} not found.')

# execute PrusaSlicer and create gcode from provided STL file
print_msg('Execute slicer:\n')
subprocess.run([
    SLICER_APP_EXECUTABLE,           # prusa slicer executable
    '-g',                            # export gcode
    inputfile,                       # absolute filepath to STL file
    '--load', SLICER_CONFIG_FILE,    # slicer .ini file
    '--output', GCODE_OUTPUT_FILE])  # absolute filepath to output Gcode file

# upload file to Karmen
print_msg('Upload file to Karmen...')
upload_url = f'{KARMEN_API_URL}/groups/{KARMEN_GROUP_ID}/api/files/local'
response = requests.post(
    upload_url,
    headers={'Accept': 'application/json', 'x-api-key': KARMEN_API_KEY},
    files={'file': (inputfile + '.gcode', open(GCODE_OUTPUT_FILE, 'rb'))})
if response.status_code == 201:
    print_msg(f'File {GCODE_OUTPUT_FILE} uploaded.')

    # assign file in gcode to print queue
    file_id = response.json()['files']['local']['x-id']
    print_msg('Assign file to PrintQueue...')
    print_queue_url = f'{KARMEN_API_URL}/groups/{KARMEN_GROUP_ID}/print-queue/'
    queue_response = requests.post(
        print_queue_url,
        headers={'Accept': 'application/json', 'x-api-key': KARMEN_API_KEY},
        json={
            'file': file_id,
            'state': 'to-be-printed',
            'jobox_autostart': False
        })
    if queue_response.status_code == 201:
        print_msg('Assigned.')
    else:
        on_error(f'Error when assigning file to PrintQueue. Server response: HTTP {queue_response.status_code} {queue_response.reason}.')
else:
    on_error(f'Error when uploading file to Karmen. Server response: HTTP {response.status_code} {response.reason}.')


print_msg(f'All done!')

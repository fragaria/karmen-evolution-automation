import sys
import subprocess
import requests

from settings import SLICER_APP_EXECUTABLE, SLICER_CONFIG_FILE, \
    KARMEN_GROUP_ID, KARMEN_API_KEY, KARMEN_API_URL


def on_error(msg):
    print_msg(f'ERROR: {msg}', bold=True)
    sys.exit()


def print_msg(msg, bold=False):
    if bold:
        print(f'\n\033[1m{msg}\033[0m')
    else:
        print(f'{msg}')


def slice_stl(input_file, output_file):
    subprocess.run([
        SLICER_APP_EXECUTABLE,           # prusa slicer executable
        '-g',                            # export gcode
        input_file,                      # absolute filepath to STL file
        '--load', SLICER_CONFIG_FILE,    # slicer .ini file
        '--output', output_file])        # absolute filepath to output Gcode file


def upload_file_to_karmen(file_name, input_file):
    print_msg('Upload file to Karmen...')
    upload_url = f'{KARMEN_API_URL}/groups/{KARMEN_GROUP_ID}/api/files/local'
    print(upload_url)
    response = requests.post(
        upload_url,
        headers={'Accept': 'application/json', 'x-api-key': KARMEN_API_KEY},
        files={'file': (file_name, open(input_file, 'rb'))})
    if response.status_code == 201:
        print_msg(f'File uploaded.')

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

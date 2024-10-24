import os
import pathlib

from utils import upload_file_to_karmen, print_msg
from settings import GCODE_DIR


def upload_all_func():
    gcode_files = os.listdir(GCODE_DIR)

    for file in gcode_files:
        file_path = pathlib.Path(os.path.join(GCODE_DIR, file))
        if file_path.suffix != '.UPLOADED': # skip .UPLOADED files
            print_msg(f'Processing file: {file_path}')

            if file_path.suffix != '.gcode':
                print_msg(f'  - Skip uknown file type.')

            elif file_path.suffix == '.gcode':
                if f'{file}.UPLOADED' in gcode_files:
                    print_msg(f'  - Skip - file is already uploaded.')
                else:
                    print_msg(f'  - Going to upload file to Karmen...')
                    upload_file_to_karmen(file_path.name, file_path)
                    open(f'{file_path}.UPLOADED', 'a').close()


if __name__ == '__main__':
    upload_all_func()

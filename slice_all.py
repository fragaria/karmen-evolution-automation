import os
import pathlib

from utils import slice_stl, print_msg

from settings import STL_DIR, GCODE_DIR


def slice_all_func():
    stl_files = os.listdir(STL_DIR)
    gcode_files = os.listdir(GCODE_DIR)

    for stl_file in stl_files:
        stl_path = pathlib.Path(os.path.join(STL_DIR, stl_file))
        if stl_path.suffix != '.stl':
            raise Exception(f'Invalid file in STL directory: {stl_file}. It\'s not STL file.')

        print_msg(f'Processing file: {stl_file}')

        gcode_file = str(stl_path.stem) + '.gcode'
        if gcode_file in gcode_files:
            print_msg(f'  - Skipping, Gcode already exists.')
        else:
            gcode_path = os.path.join(GCODE_DIR, gcode_file)
            print_msg(f'  - Going to generate new gcode file: {gcode_path}')
            slice_stl(stl_path, gcode_path)


if __name__ == '__main__':
    slice_all_func()

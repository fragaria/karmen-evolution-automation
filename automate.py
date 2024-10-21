from utils import print_msg
from slice_all import slice_all_func
from upload_all import upload_all_func


print_msg('Starting automation', bold=True)

print_msg('Star slicing all STL files\n==========================', bold=True)
slice_all_func()

print_msg('Star uploading all GCODE files\n==============================', bold=True)
upload_all_func()

print_msg('All DONE!', bold=True)

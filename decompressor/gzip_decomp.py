import gzip
import os
import shutil
import datetime

filename = input("Enter filename: ")
decompressed_filename = 'decomp_' + os.path.splitext(filename)[0]

start_time = datetime.datetime.now()

with gzip.open(filename, 'rb') as file_input:
    with open(decompressed_filename, 'wb') as file_output:
        shutil.copyfileobj(file_input, file_output)

end_time = datetime.datetime.now()

time_elapsed = end_time - start_time

input('Time elapsed: ' + str(time_elapsed) + 's')
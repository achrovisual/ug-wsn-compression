import bz2
import os
import shutil
import datetime

filename = input("Enter filename: ")
decompressed_filename = 'decomp_' + os.path.splitext(filename)[0]

start_time = datetime.datetime.now()

with open(filename, 'rb') as data:
    tarbz2contents = bz2.decompress(data.read())

    fh = open(decompressed_filename, "wb")
    fh.write(tarbz2contents)
    fh.close()

end_time = datetime.datetime.now()

time_elapsed = end_time - start_time

input('Time elapsed: ' + str(time_elapsed) + 's')

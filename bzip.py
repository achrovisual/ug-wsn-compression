import bz2
import os
import shutil
import datetime

filename = input("Enter filename: ")
compressed_filename = os.path.splitext(filename)[0] + '.bz2'

start_time = datetime.datetime.now()

with open(filename, 'rb') as data:
    tarbz2contents = bz2.compress(data.read(), 9)

    fh = open(compressed_filename, "wb")
    fh.write(tarbz2contents)
    fh.close()

end_time = datetime.datetime.now()

time_elapsed = end_time - start_time

input('Time elapsed: ' + str(time_elapsed) + 's')

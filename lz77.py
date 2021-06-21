from LZ77src import LZ77Compressor

import os
import datetime

filename = input("Enter filename: ")
compressed_filename = os.path.splitext(filename)[0] + '.lz'

start_time = datetime.datetime.now()

compressor = LZ77Compressor()
compressor.compress(filename, compressed_filename)

end_time = datetime.datetime.now()

time_elapsed = end_time - start_time

input('Time elapsed: ' + str(time_elapsed) + 's')

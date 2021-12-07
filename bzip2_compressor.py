import bz2
from datetime import datetime
from os.path import getsize

from compressor import Compressor
from performance_metrics import ratio, start, stop

class bzip2_Compressor(Compressor):
    def __init__(self):
        self.name = 'bzip2'
        self.history = []
    def compress(self, filename):
        start()
        try:
            compressed_filename = filename + '.bz2'

            start_time = datetime.now()

            with open(filename, 'rb') as file_in:
                bz2_contents = bz2.compress(file_in.read(), 9)
                file_out = open(compressed_filename, "wb")
                file_out.write(bz2_contents)
                file_out.close()

            end_time = datetime.now()
            time_elapsed = end_time - start_time

            og_size = getsize(filename)
            cp_size = getsize(compressed_filename)

            compression_ratio = ratio(og_size, cp_size)
        finally:
            result = stop()
            print(result)

            self.log(filename, time_elapsed, og_size, cp_size, compression_ratio, result)

import bz2, shutil, sys, os
from datetime import datetime
from os.path import getsize
from .decompressor import Decompressor
from performance_metrics import ratio, start, stop

class bzip2(Decompressor):
    def __init__(self):
        self.name = 'bzip2'
        self.history = []

    def decompress(self, filename, data):
        try:
            start_time = datetime.now()

            cp_size = sys.getsizeof(data)
            decompressed_data = bz2.decompress(data)

            end_time = datetime.now()
            time_elapsed = end_time - start_time

            og_size = sys.getsizeof(decompressed_data)

            # with open(filename, 'rb') as data:
            #     tarbz2contents = bz2.decompress(data.read())

            #     fh = open(decompressed_filename, "wb")
            #     fh.write(tarbz2contents)
            #     fh.close()

            # end_time = datetime.now()
            # time_elapsed = end_time - start_time

            # og_size = getsize(decompressed_filename)
            # cp_size = getsize(filename)

            compression_ratio = ratio(og_size, cp_size)
        finally:
            self.log(filename, time_elapsed, og_size, cp_size, compression_ratio)
            return decompressed_data

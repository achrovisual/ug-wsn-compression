import gzip, shutil, sys, os
from datetime import datetime
from os.path import getsize
from .decompressor import Decompressor
from performance_metrics import ratio, start, stop

class Gzip(Decompressor):
    def __init__(self):
        self.name = 'Gzip'
        self.history = []

    def decompress(self, filename, data):
        try:
            start_time = datetime.now()

            cp_size = sys.getsizeof(data)
            decompressed_data = gzip.decompress(data)

            end_time = datetime.now()
            time_elapsed = end_time - start_time

            og_size = sys.getsizeof(decompressed_data)


            # with gzip.open(filename, 'rb') as file_input:
            #     with open(decompressed_filename, 'wb') as file_output:
            #         shutil.copyfileobj(file_input, file_output)

            # end_time = datetime.now()
            # time_elapsed = end_time - start_time

            # og_size = getsize(decompressed_filename)
            # cp_size = getsize(filename)

            compression_ratio = ratio(og_size, cp_size)
        finally:
            self.log(filename, time_elapsed, og_size, cp_size, compression_ratio)
            return decompressed_data

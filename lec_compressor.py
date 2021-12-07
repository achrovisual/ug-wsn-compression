from datetime import datetime
from os.path import getsize

from compressor import Compressor
from lec import LECAlgorithm
from performance_metrics import ratio, start, stop

class LEC_Compressor(Compressor):
    def __init__(self):
        self.name = 'LEC'
        self.history = []
    def compress(self, filename):
        start()
        try:
            compressed_filename = filename + '.lec'

            start_time = datetime.now()

            compressor = LECAlgorithm()
            compressor.compress(filename, compressed_filename)

            end_time = datetime.now()
            time_elapsed = end_time - start_time

            og_size = getsize(filename)
            cp_size = getsize(compressed_filename)

            compression_ratio = ratio(og_size, cp_size)
        finally:
            result = stop()
            print(result)

            self.log(filename, time_elapsed, og_size, cp_size, compression_ratio, result)

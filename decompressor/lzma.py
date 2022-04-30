import shutil, sys, os
import lzma as lz
from datetime import datetime
from .decompressor import Decompressor
from performance_metrics import ratio, start, stop

class LZMA(Decompressor):
    def __init__(self):
        self.name = 'LZMA'
        self.history = []
    def decompress(self, filename, data):
        try:
            # print(data)
            start_time = datetime.now()

            cp_size = sys.getsizeof(data)
            decompressed_data = lz.decompress(data)

            end_time = datetime.now()
            time_elapsed = end_time - start_time

            og_size = sys.getsizeof(decompressed_data)

            compression_ratio = ratio(og_size, cp_size)
        finally:
            self.log(filename, time_elapsed, og_size, cp_size, compression_ratio)
            return decompressed_data

from datetime import datetime
from os.path import getsize
from os import system

from compressor import Compressor
from performance_metrics import ratio

class LZW_Compressor(Compressor):
    def __init__(self):
        self.name = 'LZW'
        self.history = []
    def compress(self, filename):
        compressed_filename = filename + '.Z'
        og_size = getsize(filename)
        start_time = datetime.now()
        system(f"compress '{filename}'")
        end_time = datetime.now()
        time_elapsed = end_time - start_time

        cp_size = getsize(compressed_filename)

        compression_ratio = ratio(og_size, cp_size)



        self.log(filename, time_elapsed, og_size, cp_size, compression_ratio)

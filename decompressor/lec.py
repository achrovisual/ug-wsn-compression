import shutil, sys, os
from datetime import datetime
from os.path import getsize
from .decompressor import Decompressor
from performance_metrics import ratio, start, stop
from algorithm.lec import LECAlgorithm

class LEC(Decompressor):
    def __init__(self):
        self.name = 'LEC'
        self.history = []
    def decompress(self, filename, data):
        try:
            start_time = datetime.now()
            
            cp_size = len(data)
            decompressed_data = LECAlgorithm().decompress(None, data)
            
            end_time = datetime.now()
            time_elapsed = end_time - start_time

            og_size = sys.getsizeof(decompressed_data)
            
            compression_ratio = ratio(og_size, cp_size)

        finally:
            self.log(filename, time_elapsed, og_size, cp_size, compression_ratio)
            return decompressed_data

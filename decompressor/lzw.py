import shutil, sys, os
from datetime import datetime
from os.path import getsize
from .decompressor import Decompressor
from performance_metrics import ratio, start, stop

class LZW(Decompressor):
    def __init__(self):
        self.name = 'LZW'
        self.history = []
    def decompress(self, filename):
        try:
            decompressed_filename = os.path.splitext(filename)[0]
            start_time = datetime.now()

            os.system("uncompress %s" % filename)

            end_time = datetime.now()
            time_elapsed = end_time - start_time

            og_size = getsize(decompressed_filename)
            cp_size = getsize(filename)

            compression_ratio = ratio(og_size, cp_size)
        finally:
            self.log(filename, time_elapsed, og_size, cp_size, compression_ratio)

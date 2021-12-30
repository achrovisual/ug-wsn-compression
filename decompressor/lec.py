# import pyRAPL
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
    def decompress(self, filename):
        try:
            # decompressed_filename = self.name + '_' + os.path.splitext(filename)[0]
            decompressed_filename = os.path.splitext(filename)[0]
            start_time = datetime.now()

            LECAlgorithm().decompress(filename, decompressed_filename)

            end_time = datetime.now()
            time_elapsed = end_time - start_time

            og_size = getsize(decompressed_filename)
            cp_size = getsize(filename)

            compression_ratio = ratio(og_size, cp_size)
        finally:
            self.log(filename, time_elapsed, og_size, cp_size, compression_ratio)

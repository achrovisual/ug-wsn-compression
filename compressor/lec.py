# import pyRAPL
from datetime import datetime
from os.path import getsize

from .compressor import Compressor
from algorithm.lec import LECAlgorithm
from performance_metrics import ratio, start, stop

class LEC(Compressor):
    def __init__(self):
        self.name = 'LEC'
        self.history = []
    def compress(self, filename):
        start()
        # pyRAPL.setup()
        # meter = pyRAPL.Measurement('bar')
        # meter.begin()
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
            # meter.end()
            result = stop()
            # result.append((meter.result.pkg[0]/1000000)/(meter.result.duration/1000000))
            # result.append((meter.result.dram[0]/1000000)/(meter.result.duration/1000000))
            result.append(0)
            result.append(0)

            self.log(filename, time_elapsed, og_size, cp_size, compression_ratio, result)

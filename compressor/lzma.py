import lzma, platform, pyRAPL
from datetime import datetime
from os.path import getsize

from .compressor import Compressor
from performance_metrics import ratio, start, stop

class LZMA(Compressor):
    def __init__(self):
        self.name = 'LZMA'
        self.history = []
    def compress(self, filename):
        start()
        if 'Intel' in platform.processor():
            pyRAPL.setup()
            meter = pyRAPL.Measurement('bar')
            meter.begin()
        try:
            compressed_filename = filename + '.xz'

            start_time = datetime.now()

            with open(filename, 'rb') as file_in:
                lzma_contents = lzma.compress(file_in.read())
                file_out = open(compressed_filename, "wb")
                file_out.write(lzma_contents)
                file_out.close()

            end_time = datetime.now()
            time_elapsed = end_time - start_time

            og_size = getsize(filename)
            cp_size = getsize(compressed_filename)

            compression_ratio = ratio(og_size, cp_size)
        finally:
            if 'Intel' in platform.processor():
                meter.end()
            result = stop()
            if 'Intel' in platform.processor():
                result.append((meter.result.pkg[0]/1000000)/(meter.result.duration/1000000))
                result.append((meter.result.dram[0]/1000000)/(meter.result.duration/1000000))
            else:
                result.append(0)
                result.append(0)
            
            self.log(filename, time_elapsed, og_size, cp_size, compression_ratio, result)

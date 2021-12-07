import gzip, shutil, pyRAPL
from datetime import datetime
from os.path import getsize

from compressor import Compressor
from performance_metrics import ratio, start, stop

class Gzip_Compressor(Compressor):
    def __init__(self):
        self.name = 'Gzip'
        self.history = []
    def compress(self, filename):
        start()
        pyRAPL.setup()
        meter = pyRAPL.Measurement('bar')
        meter.begin()
        try:
            compressed_filename = filename + '.gz'

            start_time = datetime.now()

            with open(filename, 'rb') as file_in:
                with gzip.open(compressed_filename, 'wb') as file_out:
                    shutil.copyfileobj(file_in, file_out)

            end_time = datetime.now()
            time_elapsed = end_time - start_time

            og_size = getsize(filename)
            cp_size = getsize(compressed_filename)

            compression_ratio = ratio(og_size, cp_size)
        finally:
            meter.end()
            result = stop()
            result.append((meter.result.pkg[0]/1000000)/(meter.result.duration/1000000))
            result.append((meter.result.dram[0]/1000000)/(meter.result.duration/1000000))

            self.log(filename, time_elapsed, og_size, cp_size, compression_ratio, result)

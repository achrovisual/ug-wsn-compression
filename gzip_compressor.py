import gzip, shutil
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
            result = stop()
            print(result)

            self.log(filename, time_elapsed, og_size, cp_size, compression_ratio, result)

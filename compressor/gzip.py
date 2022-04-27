import gzip, platform, pyRAPL, cpuinfo
from datetime import datetime
from sys import getsizeof

from .compressor import Compressor
from performance_metrics import ratio, start, stop

class Gzip(Compressor):
    def __init__(self):
        self.name = 'Gzip'
        self.history = []
    def compress(self, filename, element):
        start()
        try:
            if 'Intel' in cpuinfo.get_cpu_info()['brand_raw']:
                pyRAPL.setup()
                meter = pyRAPL.Measurement('bar')
                meter.begin()
        except Exception as e:
            pass
            # print(e)
            # print("pyRAPL not initialized.")
        try:
            start_time = datetime.now()

            compressed_data = gzip.compress(element["data"], 9)

            end_time = datetime.now()
            time_elapsed = end_time - start_time

            og_size = element["size"]
            cp_size = getsizeof(compressed_data)

            compression_ratio = ratio(og_size, cp_size)
        finally:
            try:
                if 'Intel' in  cpuinfo.get_cpu_info()['brand_raw']:
                    meter.end()
            except:
                pass
            result = stop()
            try:
                if 'Intel' in  cpuinfo.get_cpu_info()['brand_raw']:
                    result.append((meter.result.pkg[0]/1000000)/(meter.result.duration/1000000))
                    result.append((meter.result.dram[0]/1000000)/(meter.result.duration/1000000))
                else:
                    result.append(0)
                    result.append(0)
            except:
                result.append(0)
                result.append(0)
            self.log(filename + "_" + str(element["block"]), time_elapsed, og_size, cp_size, compression_ratio, result)
            return compressed_data

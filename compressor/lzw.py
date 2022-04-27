import platform, pyRAPL, cpuinfo
from datetime import datetime
from os.path import getsize
from os import system

from .compressor import Compressor
from performance_metrics import ratio, start_system_wide, stop

class LZW(Compressor):
    def __init__(self):
        self.name = 'LZW'
        self.history = []
    def compress(self, filename):
        start_system_wide()
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
            compressed_filename = filename + '.Z'
            og_size = getsize(filename)
            start_time = datetime.now()
            system(f"compress '{filename}'")
            end_time = datetime.now()
            time_elapsed = end_time - start_time

            cp_size = getsize(compressed_filename)

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

            self.log(filename, time_elapsed, og_size, cp_size, compression_ratio, result)

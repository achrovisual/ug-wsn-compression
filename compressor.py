from datetime import datetime
from os.path import exists
from numpy import mean

class Compressor:
    def log(self, filename, compression_time, original_size, compressed_size, compression_ratio, system_utilization):
        cpu_usage = mean(system_utilization[0])
        memory_usage = mean(system_utilization[1])
        cpu_power_consumption = system_utilization[2]
        ram_power_consumption = system_utilization[3]
        index = len(self.history)
        log_time = datetime.now()
        log_message = "[%d] %s - Compressed %s using %s. Time elapsed: %ss. Original size: %s B. Compressed size: %s B. Compression ratio: %.2f%%. CPU usage: %.2f%%. Memory usage: %.2f%%. CPU power consumption: %.2fW. RAM power consumption: %.2fW\n" % (index, log_time, filename, self.name, compression_time, original_size, compressed_size, compression_ratio, cpu_usage, memory_usage, cpu_power_consumption, ram_power_consumption)
        self.history.append(log_message)

        date = log_time.strftime("%d-%m-%Y")
        log_filename = 'log %s.txt' % (date)

        if exists(log_filename):
            log_file = open(log_filename, 'a')
        else:
            log_file = open(log_filename, 'w')

        log_file.write(log_message)
        log_file.close()

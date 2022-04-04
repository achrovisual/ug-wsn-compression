import csv
from datetime import datetime
from os.path import exists
from numpy import mean

class Compressor:
    def log(self, filename, compression_time, original_size, compressed_size, compression_ratio, system_utilization):
        cpu_usage = mean(system_utilization[0])
        memory_usage = mean(system_utilization[1])
        cpu_power_consumption = system_utilization[2]
        ram_power_consumption = system_utilization[3]
        log_time = datetime.now()

        date = log_time.strftime("%Y-%m-%d")
        log_filename = 'comp %s.csv' % (date)

        header = ['timestamp', 'filename', 'algorithm', 'time taken', 'original size', 'compressed size', 'compression ratio', 'cpu usage', 'memory usage', 'cpu power consumption', 'ram power consumption']
        data = [log_time, filename, self.name, compression_time, original_size, compressed_size, compression_ratio, cpu_usage, memory_usage, cpu_power_consumption, ram_power_consumption]

        if exists(log_filename):
            log_file = open(log_filename, 'a')
            writer = csv.writer(log_file)
            writer.writerow(data)
        else:
            log_file = open(log_filename, 'w', newline='')
            writer = csv.writer(log_file)
            writer.writerow(header)
            writer.writerow(data)

        log_file.close()

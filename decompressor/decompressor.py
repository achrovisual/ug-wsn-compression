import csv
from datetime import datetime
from os.path import exists

class Decompressor:
    def log(self, filename, decompression_time, original_size, compressed_size, compression_ratio):
        log_time = datetime.now()

        date = log_time.strftime("%Y-%m-%d")
        log_filename = 'decomp %s.csv' % (date)

        header = ['timestamp', 'filename', 'algorithm', 'time taken', 'decompressed size', 'compressed size', 'compression ratio']
        data = [log_time, filename, self.name, decompression_time, original_size, compressed_size, compression_ratio]

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

import csv
from datetime import datetime
from os.path import exists

class Decompressor:
    def log(self, filename, decompression_time, original_size, compressed_size, compression_ratio):
        # index = len(self.history)
        log_time = datetime.now()
        # log_message = "[%d] %s - Decompressed %s using %s. Time elapsed: %ss. Original size: %s B. Compressed size: %s B. Compression ratio: %.2f%%\n" % (index, log_time, filename, self.name, compression_time, original_size, compressed_size, compression_ratio)
        # self.history.append(log_message)

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

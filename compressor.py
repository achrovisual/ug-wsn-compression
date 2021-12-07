from datetime import datetime
from os.path import exists

class Compressor:
    def log(self, filename, compression_time, original_size, compressed_size, compression_ratio):
        # , compression_time, system_utilization, compression_ratio, data_integrity
        index = len(self.history)
        log_time = datetime.now()
        log_message = "[%d] %s - Compressed %s using %s. Time elapsed: %ss. Original size: %s B. Compressed size: %s B. Compression ratio: %.2f%%.\n" % (index, log_time, filename, self.name, compression_time, original_size, compressed_size, compression_ratio)
        self.history.append(log_message)

        date = log_time.strftime("%d-%m-%Y")
        log_filename = 'log %s.txt' % (date)

        if exists(log_filename):
            log_file = open(log_filename, 'a')
        else:
            log_file = open(log_filename, 'w')

        log_file.write(log_message)
        log_file.close()

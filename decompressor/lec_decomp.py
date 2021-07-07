import os
import datetime
import lec

filename = input("Enter filename: ")
compressed_filename = os.path.splitext(filename)[0]

start_time = datetime.datetime.now()

lec.decompress(filename, compressed_filename)

end_time = datetime.datetime.now()

time_elapsed = end_time - start_time

input('Time elapsed: ' + str(time_elapsed) + 's')

import os
import shutil
import datetime

filename = input("Enter filename: ")

start_time = datetime.datetime.now()

os.system("uncompress %s" % filename)

end_time = datetime.datetime.now()

time_elapsed = end_time - start_time

input('Time elapsed: ' + str(time_elapsed) + 's')

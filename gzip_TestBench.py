import gzip
import shutil
import datetime
filename = input("FILE NAME:\t")
modName = filename + '.out.gz'
beforeCOMP = datetime.datetime.now()
with open(filename, 'rb') as fileIN:
    with gzip.open(modName, 'wb') as fileOUT:
        shutil.copyfileobj(fileIN, fileOUT)

afterCOMP = datetime.datetime.now()

diff = afterCOMP - beforeCOMP

input(diff)
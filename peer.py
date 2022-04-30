import os, sys, serial, tqdm
from decompressor.bzip import bzip2
from decompressor.gzip import Gzip
from decompressor.lec import LEC
from decompressor.lzma import LZMA
from decompressor.lzw import LZW
from performance_metrics import integrity

SEPARATOR = "<SEPARATOR>"

xbee = serial.Serial('/dev/ttyUSB0', 9600)
print(f'[+] Connected to Xbee.')
count = 0

while True:
    while xbee.in_waiting < 0:
        pass
    received = xbee.readline()
    print(received)
    received = received.decode()[:-1]
    print(received)
    algorithm, filesize, md5 = received.split(SEPARATOR)
    if algorithm != 'lec':
        filesize = int(filesize) + 16
    else:
        filesize = int(filesize) -24
    data = b''
    decomp_data = None

    # print(filesize)

    progress = tqdm.tqdm(range(filesize), f"Receiving sensor readings", unit="B", unit_scale=True, unit_divisor=1024)

    if algorithm != 'lzw':
        count = 0

    while True:
        # print(sys.getsizeof(data))
        # print(xbee.in_waiting)
        # print(sys.getsizeof(data))
        # if xbee.in_waiting > 0:
        bytes_read = xbee.read()
        # filesize = filesize - sys.getsizeof(bytes_read)
        data += bytes_read
        progress.update(sys.getsizeof(bytes_read))

        if filesize == sys.getsizeof(data):
            print(sys.getsizeof(data))
            # print(data)
            if algorithm == 'lzma':
                lzma_comp = LZMA()
                decomp_data = lzma_comp.decompress(None, data)
            elif algorithm == 'lzw':
                temp = "normalized.csv" + '_' + str(count)

                with open(temp+'.Z', "wb") as file_in:
                    file_in.write(data)
                    file_in.close()

                lzw_comp = LZW()
                lzw_comp.decompress(temp+'.Z', temp)

                with open(temp, 'rb') as f:
                    decomp_data = f.read()

                count = count + 1
            elif algorithm == 'bzip2':
                bz_comp = bzip2()
                decomp_data = bz_comp.decompress(None, data)
            elif algorithm == 'gzip':
                gz_comp = Gzip()
                decomp_data = gz_comp.decompress(None, data)
            elif algorithm == 'lec':
                lec_comp = LEC()
                decomp_data = lec_comp.decompress(None, data)

            md5_decomp = integrity(None, decomp_data)
            if md5 == md5_decomp:
                print('\nMD5 verified.')
            else:
                print('\nMD5 verification failed.')
            break

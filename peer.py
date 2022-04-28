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

while True:
    while xbee.in_waiting < 0:
        pass
    received = xbee.readline().decode()[:-1]
    print(received)
    algorithm, filesize, md5 = received.split(SEPARATOR)
    filesize = int(filesize)
    data = b''
    decomp_data = None

    progress = tqdm.tqdm(range(filesize), f"Receiving sensor readings", unit="B", unit_scale=True, unit_divisor=1024)

    while True:
        if xbee.in_waiting > 0:
            bytes_read = xbee.read()
            filesize = filesize - len(bytes_read)
            data += bytes_read
            progress.update(len(bytes_read))
        if filesize <= 0:
            if algorithm == 'lzma':
                lzma_comp = LZMA()
                decomp_data = lzma_comp.decompress(None, data)
            elif algorithm == 'lzw':
                with open("temp.Z", "wb") as file_in:
                    file_in.write(data)
                lzw_comp = LZW()
                lzw_comp.decompress(temp)
                with open('temp', 'rb') as f:
                    decomp_data = f.read()
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
                print('MD5 verified.')
            else:
                print('MD5 verification failed.')
            break
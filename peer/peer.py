import os, sys, serial, tqdm
sys.path.append('C:\\Users\\JKGC\\Desktop\\ug-wsn-compression\\decompressor')
from bzip_decomp import bzip2_Decompressor
from gzip_decomp import Gzip_Decompressor
from lec_decomp import LEC_Decompressor
from lzma_decomp import LZMA_Decompressor
from lzw_decomp import LZW_Decompressor
sys.path.append('C:\\Users\\JKGC\\Desktop\\ug-wsn-compression')
from performance_metrics import integrity

SEPARATOR = "<SEPARATOR>"

xbee = serial.Serial('COM4', 9600)
print(f'[+] Connected to Xbee.')

while True:
    if xbee.in_waiting > 0:
        break
received = xbee.readline().decode()
filename, filesize, md5 = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)
ext = os.path.splitext(filename)[-1].lower()

progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        if xbee.in_waiting > 0:
            bytes_read = xbee.read()
            filesize = filesize - len(bytes_read)
            f.write(bytes_read)
            progress.update(len(bytes_read))
        if filesize == 0:
            break
    f.close()
    xbee.close()
    
if 'xz' in ext:
    lzma_comp = LZMA_Decompressor()
    lzma_comp.decompress(filename)
    # decompressed_filename = 'LZMA_' + os.path.splitext(filename)[0]
    decompressed_filename = os.path.splitext(filename)[0]
    md5_decomp = integrity(decompressed_filename)
elif 'bz2' in ext:
    bzip2_comp = bzip2_Decompressor()
    bzip2_comp.decompress(filename)
    # decompressed_filename = 'bzip2_' + os.path.splitext(filename)[0]
    decompressed_filename = os.path.splitext(filename)[0]
    md5_decomp = integrity(decompressed_filename)
elif 'gz' in ext:
    gzip_comp = Gzip_Decompressor()
    gzip_comp.decompress(filename)
    # decompressed_filename = 'Gzip_' + os.path.splitext(filename)[0]
    decompressed_filename = os.path.splitext(filename)[0]
    md5_decomp = integrity(decompressed_filename)
elif 'z' in ext:
    lzw_comp = LZW_Decompressor()
    lzw_comp.decompress(filename)
    # decompressed_filename = 'LZW_' + os.path.splitext(filename)[0]
    decompressed_filename = os.path.splitext(filename)[0]
    md5_decomp = integrity(decompressed_filename)
elif 'lec' in ext:
    lec_comp = LEC_Decompressor()
    lec_comp.decompress(filename)
    # decompressed_filename = 'LEC_' + os.path.splitext(filename)[0]
    decompressed_filename = os.path.splitext(filename)[0]
    md5_decomp = integrity(decompressed_filename)

print(md5)
print(md5_decomp)
if md5 == md5_decomp:
    print('MD5 verified.')
else:
    print('MD5 verification failed!')
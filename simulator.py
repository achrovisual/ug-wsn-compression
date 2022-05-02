import serial, os, datetime, shutil, tqdm, sys, time
from compressor.lzma import LZMA
from compressor.lzw import LZW
from compressor.lec import LEC
from compressor.bzip2 import bzip2
from compressor.gzip import Gzip
from performance_metrics import integrity

def process_data(filename, frequency):
    file_in = open(filename, 'rb')
    raw = file_in.readlines()

    buffer = []

    start = 0
    end = frequency
    count = 0

    while not end == len(raw):

        temp = b''.join(raw[start:end])
        hash = integrity(None, temp)
        buffer.append({"block": count, "size": sys.getsizeof(temp), "checksum": hash, "data": temp})

        start = start + frequency
        end = end + frequency
        count = count + 1

        if end > len(raw):
            end = len(raw)
            # print(start - end)

    return buffer

def clrscr():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    else:
        pass

def main():
    try:
        SEPARATOR = '<SEPARATOR>'
        BUFFER_SIZE = 4096 # send 4096 bytes each time step

        lzma_comp = LZMA()
        lzw_comp = LZW()
        lec_comp = LEC()
        bzip2_comp = bzip2()
        gzip_comp = Gzip()

        try:
            xbee = serial.Serial('/dev/ttyUSB0', 9600)
            print('[+] Connected to XBee.')
            input('Press any key to continue...')
            clrscr()
        except:
            print('[-] Cannot connect to XBee.')
            input('Press any key to continue...')
            # sys.exit(0)

        try:
            filename = input('Enter filename for compression: ')
            frequency = int(input('Enter frequency (Hz): '))


            # Prepare data and split into a list based on the frequency provided
            # List elements are dictionary objects. The structure is as follows:
            # {"block": value, "size": value, "checksum"" value, "data": value}
            original_data = process_data(filename, frequency)

            og_file_size = os.path.getsize(filename)

            print('[+] File found!')
            input('Press any key to continue...')
            clrscr()

            # md5 = integrity(filename)
            print(f'File to compress: {filename} ({og_file_size} B)')
            # print(f'MD5 Hash: {md5}')
            print("Compression algorithms:\n1. LZMA\n2. LZW\n3. bzip2\n4. gzip\n5. lec")
            choice = input("Choice: ")
            compressed_file = ''
            cp_file_size = ''

            if choice == '1':
                for element in original_data:
                    # Compress binary string, output is a dictionary containing compressed file size and the data
                    compressed = lzma_comp.compress(filename, element)
                    algo = 'lzma'
                    xbee.write(f'{algo}{SEPARATOR}{sys.getsizeof(compressed)}{SEPARATOR}{element["checksum"]}\n'.encode())
                    progress = tqdm.tqdm(range(sys.getsizeof(compressed)), f'Sending {frequency} readings', unit="B", unit_scale=True, unit_divisor=1024)
                    xbee.write(compressed)
                    progress.update(sys.getsizeof(compressed))
            elif choice == '2':
                # Since LZW can't accept standard input, we have to write the binary strings into files to work around it. Append the filenames into a list.
                for index, element in enumerate(original_data, start = 0):
                    try:
                        temp = filename + '_' + str(index)
                        with open(temp, "wb") as file_in:
                            file_in.write(element["data"])
                            file_in.close()
                        lzw_comp.compress(temp)
                        with open(temp + '.Z', 'rb') as f:
                            data = f.read()
                            algo = 'lzw'
                            xbee.write(f'{algo}{SEPARATOR}{sys.getsizeof(data)}{SEPARATOR}{element["checksum"]}\n'.encode())
                            progress = tqdm.tqdm(range(sys.getsizeof(data)), f'Sending {frequency} readings', unit="B", unit_scale=True, unit_divisor=1024)
                            xbee.write(data)
                            progress.update(sys.getsizeof(data))
                            f.close()
                    except Exception as e:
                        print(e)
            elif choice == '3':
                for element in original_data:
                    # Compress binary string, output is a dictionary containing compressed file size and the data
                    compressed = bzip2_comp.compress(filename, element)
                    algo = 'bzip2'
                    xbee.write(f'{algo}{SEPARATOR}{sys.getsizeof(compressed)}{SEPARATOR}{element["checksum"]}\n'.encode())
                    progress = tqdm.tqdm(range(sys.getsizeof(compressed)), f'Sending {frequency} readings', unit="B", unit_scale=True, unit_divisor=1024)
                    xbee.write(compressed)
                    progress.update(sys.getsizeof(compressed))
            elif choice == '4':
                for element in original_data:
                    # Compress binary string, output is a dictionary containing compressed file size and the data
                    compressed = gzip_comp.compress(filename, element)
                    algo = 'gzip'
                    xbee.write(f'{algo}{SEPARATOR}{sys.getsizeof(compressed)}{SEPARATOR}{element["checksum"]}\n'.encode())
                    progress = tqdm.tqdm(range(sys.getsizeof(compressed)), f'Sending {frequency} readings', unit="B", unit_scale=True, unit_divisor=1024)
                    xbee.write(compressed)
                    progress.update(sys.getsizeof(compressed))
            elif choice == '5':
                for element in original_data:
                    # Compress binary string, output is a dictionary containing compressed file size and the data
                    compressed = lec_comp.compress(filename, element)
                    print(bytes(compressed))
                    # print(sys.getsizeof(compressed))
                    algo = 'lec'
                    xbee.write(f'{algo}{SEPARATOR}{sys.getsizeof(bytes(compressed))}{SEPARATOR}{element["checksum"]}\n'.encode())
                    progress = tqdm.tqdm(range(sys.getsizeof(compressed)), f'Sending {frequency} readings', unit="B", unit_scale=True, unit_divisor=1024)
                    xbee.write(compressed)
                    progress.update(sys.getsizeof(compressed))
        except Exception as e:
            print(e)
            print('[-] File not found.')
            input('Press any key to continue...')

        xbee.close()
    except Exception as e:
        print(e)
        xbee.close()
        sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt():
        print('Keyboard interrupt')
        sys.exit(0)

import serial, os, datetime, shutil, tqdm, sys
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
    end = frequency - 1
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

        # try:
        #     # xbee = serial.Serial('/dev/ttyUSB0', 9600)
        #     print('[+] Connected to XBee.')
        #     input('Press any key to continue...')
        #     clrscr()
        # except:
        #     print('[-] Cannot connect to XBee.')
        #     input('Press any key to continue...')
        #     sys.exit(0)

        try:
            filename = input('Enter filename for compression: ')
            frequency = int(input('Enter frequency (Hz): '))


            # Prepare data and split into a list based on the frequency provided
            # List elements are dictionary objects. The structure is as follows:
            # {"block": value, "size": value, "checksum"" value, "data": value}
            original_data = process_data(filename, frequency)

            # og_file_size = os.path.getsize(filename)

            print('[+] File found!')
            input('Press any key to continue...')
            clrscr()

            # md5 = integrity(filename)
            # print(f'File to compress: {filename} ({og_file_size} B)')
            # print(f'MD5 Hash: {md5}')
            print("Compression algorithms:\n1. LZMA\n2. LZW\n3. bzip2\n4. gzip\n5. lec")
            choice = input("Choice: ")
            compressed_file = ''
            cp_file_size = ''

            if choice == '1':
                for element in original_data:
                    # Compress binary string, output is a dictionary containing compressed file size and the data
                    compressed = lzma_comp.compress(filename, element)
                try:
                    # compressed_file = filename + '.xz'
                    # cp_file_size = os.path.getsize(compressed_file)
                    input('Press any key to continue...')
                except:
                    print('File is left uncompressed.')
                    compressed_file = filename
                    input('Press any key to continue...')
            elif choice == '2':
                filenames = []
                count = 0

                # Since LZW can't accept standard input, we have to write the binary strings into files to work around it. Append the filenames into a list.
                for element in original_data:
                    temp = filename + '_' + str(count)
                    filenames.append(temp)
                    with open(temp, "wb") as file_in:
                        file_in.write(element["data"])
                        file_in.close()
                    count = count + 1

                # Compress filenames in the list.
                for file in filenames:
                    lzw_comp.compress(file)

                try:
                    # compressed_file = file + '.Z'
                    # cp_file_size = os.path.getsize(compressed_file)
                    input('Press any key to continue...')
                except:
                    print('File is left uncompressed.')
                    compressed_file = filename
                    input('Press any key to continue...')
            elif choice == '3':
                for element in original_data:
                    # Compress binary string, output is a dictionary containing compressed file size and the data
                    compressed = bzip2_comp.compress(filename, element)
                try:
                    # compressed_file = filename + '.bz2'
                    # cp_file_size = os.path.getsize(compressed_file)
                    input('Press any key to continue...')
                except:
                    print('File is left uncompressed.')
                    compressed_file = filename
                    input('Press any key to continue...')
            elif choice == '4':
                for element in original_data:
                    # Compress binary string, output is a dictionary containing compressed file size and the data
                    compressed = gzip_comp.compress(filename, element)
                try:
                    # compressed_file = filename + '.gz'
                    # cp_file_size = os.path.getsize(compressed_file)
                    input('Press any key to continue...')
                except:
                    print('File is left uncompressed.')
                    compressed_file = filename
                    input('Press any key to continue...')
            elif choice == '5':
                for element in original_data:
                    # Compress binary string, output is a dictionary containing compressed file size and the data
                    compressed = lec_comp.compress(filename, element)
                try:
                    # compressed_file = filename + '.lec'
                    # cp_file_size = os.path.getsize(compressed_file)
                    input('Press any key to continue...')
                except:
                    print('File is left uncompressed.')
                    compressed_file = filename
                    input('Press any key to continue...')
        except Exception as e:
            print(e)
            print('[-] File not found.')
            input('Press any key to continue...')

        # if compressed_file == filename: # Compression failed
        #     xbee.write(f'{filename}{SEPARATOR}{og_file_size}{SEPARATOR}{md5}\n'.encode())
        #     progress = tqdm.tqdm(range(og_file_size), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        # else:
        #     xbee.write(f'{compressed_file}{SEPARATOR}{cp_file_size}{SEPARATOR}{md5}\n'.encode())
        #     progress = tqdm.tqdm(range(cp_file_size), f"Sending {compressed_file}", unit="B", unit_scale=True, unit_divisor=1024)
        #
        # with open(compressed_file, 'rb') as f:
        #     while True:
        #         bytes_read = f.read(BUFFER_SIZE)
        #         if not bytes_read:
        #             break
        #         xbee.write(bytes_read)
        #         progress.update(len(bytes_read))
        # xbee.close()
    except Exception as e:
        print(e)
        # xbee.close()
        sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt():
        print('Keyboard interrupt')
        sys.exit(0)

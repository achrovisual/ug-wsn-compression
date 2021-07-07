import socket, os, datetime, shutil, tqdm, sys

import bz2
import gzip as gz
import lzma as lz

def lzma(filename):
    compressed_filename = filename + '.xz'

    start_time = datetime.datetime.now()

    with open(filename, 'rb') as data:
        lzcontents = lz.compress(data.read())
        fh = open(compressed_filename, "wb")
        fh.write(lzcontents)
        fh.close()

    end_time = datetime.datetime.now()
    time_elapsed = end_time - start_time
    print(f'File: {filename}\nCompression algorithm: LZMA\nCompression time: ' + str(time_elapsed) + 's')

def lzw(filename):
    start_time = datetime.datetime.now()
    os.system(f'compress {filename}')
    end_time = datetime.datetime.now()
    time_elapsed = end_time - start_time
    print(f'File: {filename}\nCompression algorithm: LZW\nCompression time: ' + str(time_elapsed) + 's')

def bzip2(filename):
    compressed_filename = filename + '.bz2'

    start_time = datetime.datetime.now()
    with open(filename, 'rb') as data:
        tarbz2contents = bz2.compress(data.read(), 9)
        fh = open(compressed_filename, "wb")
        fh.write(tarbz2contents)
        fh.close()
    end_time = datetime.datetime.now()
    time_elapsed = end_time - start_time
    print(f'File: {filename}\nCompression algorithm: bzip2\nCompression time: ' + str(time_elapsed) + 's')

def gzip(filename):
    compressed_filename = filename + '.gz'

    start_time = datetime.datetime.now()
    with open(filename, 'rb') as file_in:
        with gz.open(compressed_filename, 'wb') as file_out:
            shutil.copyfileobj(file_in, file_out)
    end_time = datetime.datetime.now()
    time_elapsed = end_time - start_time
    print(f'File: {filename}\nCompression algorithm: gzip\nCompression time: ' + str(time_elapsed) + 's')

if __name__ == '__main__':
    try:
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step

        client = None

        try:
            SERVER = "127.0.0.1"
            PORT = 42069
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER, PORT))
            print(f"[+] Connecting to {SERVER}:{PORT}.")
            print("[+] Connected.")
            input("Press any key to continue...")
            os.system('clear')

        except:
            print(f"[+] Cannot connect to peer on {SERVER}:{PORT}.")
            input("Press any key to continue...")
            # sys.exit()


        try:
            filename = input("Enter filename for compression: ")
            og_file_size = os.path.getsize(filename)
            print(f"[+] File found!")
            input("Press any key to conitnue...")
            os.system('clear')
            print(f'File to compress: {filename} ({og_file_size} B)')
            print("Compression algorithms:\n1. LZMA\n2. LZW\n3. bzip2\n4. gzip")
            choice = input("Choice: ")

            compressed_file = ''
            if choice == '1':
                os.system('clear')
                lzma(filename)
                cp_file_size = os.path.getsize(filename + '.xz')
                print(f'Original size: {og_file_size} B\nCompressed size: {cp_file_size} B')
                input('Press any key to continue...')
                compressed_file = filename + '.xz'

            elif choice == '2':
                os.system('clear')
                lzw(filename)
                try:
                    cp_file_size = os.path.getsize(filename + '.Z')
                    print(f'Original size: {og_file_size} B\nCompressed size: {cp_file_size} B')
                    input('Press any key to continue...')
                except:
                    print('File is left uncompressed.')
                    input('Press any key to continue...')

                compressed_file = filename + '.Z'

            elif choice == '3':
                os.system('clear')
                bzip2(filename)
                cp_file_size = os.path.getsize(filename + '.bz2')
                print(f'Original size: {og_file_size} B\nCompressed size: {cp_file_size} B')
                input('Press any key to continue...')
                compressed_file = filename + '.bz2'
            elif choice == '4':
                os.system('clear')
                gzip(filename)
                cp_file_size = os.path.getsize(filename + '.gz')
                print(f'Original size: {og_file_size} B\nCompressed size: {cp_file_size} B')
                input('Press any key to continue...')
                compressed_file = filename + '.gz'
        except:
            print("[+] File not found.")
            input("Press any key to continue...")

        file_size = os.path.getsize(compressed_file)

        client.send(f"{compressed_file}{SEPARATOR}{file_size}".encode())

        progress = tqdm.tqdm(range(file_size), f"Sending {compressed_file}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(compressed_file, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                client.sendall(bytes_read)
                progress.update(len(bytes_read))
        client.close()
    except Exception as e:
        print(e)
        sys.exit()

import socket, os, datetime, shutil, tqdm, sys

from lzma_compressor import LZMA_Compressor
from lzw_compressor import LZW_Compressor
from lec_compressor import LEC_Compressor
from bzip2_compressor import bzip2_Compressor
from gzip_compressor import Gzip_Compressor

if __name__ == '__main__':
    try:
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step

        client = None

        lzma_comp = LZMA_Compressor()
        lzw_comp = LZW_Compressor()
        lec_comp = LEC_Compressor()
        bzip2_comp = bzip2_Compressor()
        gzip_comp = Gzip_Compressor()

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
            print("Compression algorithms:\n1. LZMA\n2. LZW\n3. bzip2\n4. gzip\n5. lec")
            choice = input("Choice: ")

            compressed_file = ''
            if choice == '1':
                os.system('clear')
                lzma_comp.compress(filename)
                input('Press any key to continue...')
                compressed_file = filename + '.xz'

            elif choice == '2':
                os.system('clear')
                lzw_comp.compress(filename)
                try:
                    cp_file_size = os.path.getsize(filename + '.Z')
                    input('Press any key to continue...')
                except:
                    print('File is left uncompressed.')
                    input('Press any key to continue...')
                compressed_file = filename + '.Z'
            elif choice == '3':
                os.system('clear')
                bzip2_comp.compress(filename)
                input('Press any key to continue...')
                compressed_file = filename + '.bz2'
            elif choice == '4':
                os.system('clear')
                gzip_comp.compress(filename)
                input('Press any key to continue...')
                compressed_file = filename + '.gz'
            elif choice == '5':
                os.system('clear')
                lec_comp.compress(filename)
                input('Press any key to continue...')
                compressed_file = filename + '.lec'
        except Exception as e:
            print(e)
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

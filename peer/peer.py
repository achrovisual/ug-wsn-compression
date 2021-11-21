import serial
import tqdm
import os


BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# s = socket.socket()
# s.bind((SERVER_HOST, SERVER_PORT))
# s.listen(5)
# print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# client_socket, address = s.accept()
# print(f"[+] {address} is connected.")
xbee = serial.Serial('COM3', 9600)
print(f'[+] Connected to XBee.')

# received = client_socket.recv(BUFFER_SIZE).decode()
while True:
    if xbee.in_waiting > 0:
        break
received = xbee.readline().decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)
print(f'{filename} {filesize}')
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

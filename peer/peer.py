import serial
import tqdm
import os

SEPARATOR = "<SEPARATOR>"

xbee = serial.Serial('COM4', 9600)
print(f'[+] Connected to Xbee.')

while True:
    if xbee.in_waiting > 0:
        break
received = xbee.readline().decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)

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
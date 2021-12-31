import os, csv
import pandas as pd #perform pip install openpyxl
import numpy as np

filename = input("Enter filename for compression: ")

normalizedFilename = './normalized.csv'
ext = os.path.splitext(filename)[-1].lower()
try:
    if 'xls' in ext:
        fileReader = pd.read_excel (filename, engine = 'openpyxl')
        fileReader.to_csv(normalizedFilename, index = None, header = True)
    elif 'csv' in ext or 'txt' in ext:
        try:
            with open(filename, newline='') as fileIn, open(normalizedFilename, 'w') as fileOut:
                for line in fileIn:
                    line = line.replace('\r','')
                    line = line.replace(';', ',')
                    line = line.replace('\t', ',')
                    line = line.replace('|', ',')
                    fileOut.write(line)
        except Exception as e:
            print(e)
    else:
        print("File format not supported")

except Exception as e:
    print(e)
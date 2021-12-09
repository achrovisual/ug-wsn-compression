import math
import json
from bitarray import bitarray
from bitarray.util import ba2int, int2ba

class LECAlgorithm:
  MAX_BITS = 14

  def __init__(self):
    self.table = ['00', '010', '011', '100', '101', '110', '1110', '11110', '111110', '1111110', '11111110', '111111110', '1111111110', '11111111110', '111111111110']

  def compress(self, input_file_path, output_file_path=None):
    output_buffer = bitarray(endian='big')
    data = None
    prevData = None
    diff = None
    i = 0
    # read the input file
    try:
      with open(input_file_path, 'rb') as input_file:
        data = input_file.read()
    except IOError:
      print('Could not open input file ...')
      raise

    while i < len(data):
      # compute difference
      if prevData != None:
        diff = data[i] - prevData
      else:
        diff = data[i]
      # record data for next encoding
      prevData = data[i]

      # encode difference
      # extract codeword
      if diff == 0:
        numBits = 0
      else:
        numBits = self.computeBinaryLog(diff)
      code = bitarray(self.table[numBits])
      output_buffer.extend(code)

      # extract index
      if numBits != 0:
        if diff < 0:
          diff = diff - 1
          binDiff = bin(diff & 0xff)[2:]
        else:
          binDiff = bin(diff)[2:]
        posi = binDiff[len(binDiff)-numBits:len(binDiff)]
        output_buffer.extend(posi)
      
      i = i + 1
    countBits = len(output_buffer)
    missBits = output_buffer.fill()
    output_buffer[countBits:countBits+missBits] = True
    if os.path.getsize(input_file_path) > len(output_buffer)/8:
      if output_file_path:
        try:
          with open(output_file_path, 'wb') as output_file:
            output_file.write(output_buffer.tobytes())
            print('File was compressed successfully and saved to output path ...')
            return None
        except IOError:
          print('Could not write to output file path. Please check if the path is correct ...')
          raise
    else:
      return None

    # an output file path was not provided, return the compressed data
    return output_buffer

  def decompress(self, input_file_path, output_file_path=None):
    data = bitarray(endian='big')
    output_buffer = ''
    prevData = 0
    i = 2

    # read the input file
    try:
      with open(input_file_path, 'rb') as input_file:
        data.fromfile(input_file)
    except IOError:
      print('Could not open input file ...')
      raise

    while not data.all():
      matched = False
      
      # extract codeword
      while i <= self.MAX_BITS:
        try:
          numBits = self.table.index(data[:i].to01())
          matched = True
          del data[:i]
          break
        except ValueError:
          i = i + 1
        
      if matched: # extract difference
        if numBits != 0:
          if data[0] == 0:
            for x in range(numBits):
              data.invert(x)
            diff = ba2int(data[:numBits]) * -1
          else:
            diff = ba2int(data[:numBits])
          del data[:numBits]
        
          # compute for actual data
          currData = prevData + diff
        else:
          currData = prevData
        output_buffer = output_buffer + chr(currData)
        
        prevData = currData
        
        # extract next codeword
        i = 2
      else:
        print('File is possibly corrupted. Could not decompress file.')
        return None
        
    if output_file_path:
      try:
        with open(output_file_path, 'w') as output_file:
          output_file.write(output_buffer)
          print('File was decompressed successfully and saved to output path ...')
          return None
      except IOError:
        print('Could not write to output file path. Please check if the path is correct ...')
        raise
    return out_data

  def computeBinaryLog(self, diff):
    numBits = 0
    diff = abs(diff)

    while diff > 0:
      diff = diff // 2
      numBits = numBits + 1
    
    return numBits
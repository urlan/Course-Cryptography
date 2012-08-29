import sys
from Crypto.Cipher import AES
import os
import ctypes

BLOCK_SIZE = 32
IV_LENGTH = 32

# Convert String to List

def convertStringToList(string):
   list = []

   for i in range(0, len(string)):
      list.append(string[i])

   return list

# Convert List to String

def convertListToString(list):
   string = ''

   for i in range(0, len(list)):
      string += list[i]

   return string

# Increment IV List by 1

def incrIV(s, i):
   if i < 0:
      return ""

   if s[i] == 'f':
      s[i] = '0'
      s = incrIV(s, i-1)
   else:
      hex_value = int(s[i], 16)
      hex_value += 1
      s[i] = hex(hex_value)[2:];

   return s;

def strxor(a, b):
   if len(a) > len(b):
      xor_string = "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
   else:
      xor_string = "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])]) 

   return xor_string

# Decrypt a cipher text

def decrypt(key, cipher_text):

   num_blocks = len(cipher_text) / len(key)

   iv = cipher_text[0:IV_LENGTH].decode('hex')

   aes = AES.new(key.decode('hex'))
 
   index_min = IV_LENGTH
   index_max = index_min + BLOCK_SIZE

   current_xor = iv

   pt = ''

   for i in range(1, num_blocks+1):

      block_ciphered = cipher_text[index_min:index_max].decode('hex')

      block_decrypted = aes.encrypt(current_xor)

      message_block = strxor(block_decrypted, block_ciphered)

      print 'message_block'
      print message_block

      pt = pt + message_block

      list = incrIV(convertStringToList(current_xor.encode('hex')), IV_LENGTH-1)

      current_xor = convertListToString(list).decode('hex')

      print 'current_xor'
      print current_xor.encode('hex')
      print ''

      index_min = index_max
      index_max = index_max + BLOCK_SIZE

   return pt

# Main function

def main(argv):

   key = argv[1]
   cipher_text = argv[2]

   pt = decrypt(key, cipher_text)

   print '\nplain text'
   print pt
   print '\n'

   return 0

if __name__ == '__main__':
   sys.exit(main(sys.argv))

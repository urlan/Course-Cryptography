import sys
from Crypto.Cipher import AES
import os
import ctypes

BLOCK_SIZE = 32

# Xor two strings of different lengths

def strxor(a, b):
   if len(a) > len(b):
      xor_string = "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
   else:
      xor_string = "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])]) 

   return xor_string

# Decrypts a cipher text

def decrypt(key, cipher_text):

   num_blocks = len(cipher_text) / len(key)

   iv = cipher_text[0:BLOCK_SIZE].decode('hex')

   aes = AES.new(key.decode('hex'))
 
   index_min = BLOCK_SIZE
   index_max = index_min + BLOCK_SIZE

   current_xor = iv

   pt = ''

   for i in range(1, num_blocks):

      block_ciphered = cipher_text[index_min:index_max].decode('hex')

      block_decrypted = aes.decrypt(block_ciphered)

      message_block = strxor(block_decrypted, current_xor)

      pt = pt + message_block

      current_xor = block_ciphered

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

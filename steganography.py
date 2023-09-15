# steganography
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from codec import Codec, CaesarCypher, HuffmanCodes

class Steganography():
    
    def __init__(self, delimiter='#'):
        self.text = ''
        self.binary = ''
        self.delimiter = delimiter
        self.codec = None

    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein)
        print(image) # for debugging
        
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)

        # convert into binary
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            self.codec = HuffmanCodes()
        binary = self.codec.encode(message+self.delimiter)
        
        # check if possible to encode the message
        num_bytes = ceil(len(binary)//8) + 1 
        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes) 
            self.text = message
            self.binary = binary
            # your code goes here
            flattened_img = image.flatten()
            bin_str = ''
            for i in flattened_img:
                v = bin(i)
                bin_str += v
                if bin_str[-1] == 0:
                    v -= 1
                elif bin_str[-1] == 1:
                    v += 1

            # you may create an additional method that modifies the image array
            image = np.reshape(flattened_img, image.shape)
            cv2.imwrite(fileout, image)
                   
    def decode(self, filein, codec):
        image = cv2.imread(filein)
        #print(image) # for debugging      
        flag = True
        
        # convert into text
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False
        if flag:
            # your code goes here
            data = ''
            for row in image:
                for pixel in row:
                    if len(data) < len(self.binary):
                        if pixel[0] % 2 == 0:
                            data += '0'
                        else:
                            data += '1'
                        if pixel[1] % 2 == 0:
                            data += '0'
                        else:
                            data += '1'
                        if pixel[2] % 2 == 0:
                            data += '0'
                        else:
                            data += '1'
            # you may create an additional method that extract bits from the image array
            binary_data = self.codec.encode(self.text + self.delimiter)
            # update the data attributes:
            self.text = self.codec.decode(binary_data)
            self.binary = binary_data            
        
    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary)          

    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()

if __name__ == '__main__':
    
    s = Steganography()

    s.encode('fractal.jpg', 'fractal.png', 'hello', 'binary')
    # NOTE: binary should have a delimiter and text should not have a delimiter
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'

    s.decode('fractal.png', 'binary')
    print(s.text)
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'
    print('Everything works!!!')
   

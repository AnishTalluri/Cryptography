# codecs
import numpy as np

class Codec():
    
    def __init__(self, delimiter='#'):
        self.name = 'binary'
        self.delimiter = delimiter 

    # convert text or numbers into binary form    
    def encode(self, text):
        if type(text) == str:
            return ''.join([format(ord(i), "08b") for i in text])
        else:
            print('Format error')

    # convert binary data into text
    def decode(self, data):
        binary = []        
        for i in range(0,len(data),8):
            byte = data[i: i+8]
            if byte == self.encode(self.delimiter): # you need to find the correct binary form for the delimiter
                break
            binary.append(byte)
        text = ''
        for byte in binary:
            text += chr(int(byte,2))
        return text 

class CaesarCypher(Codec):

    def __init__(self, shift=3, delimiter='#'):
        self.name = 'caesar'
        self.delimiter = delimiter
        self.shift = shift    
        self.chars = 256      # total number of characters

    # convert text into binary form
    # your code should be similar to the corresponding code used for Codec
    def encode(self, text):
        data = ''
        # your code goes here
        if type(text) == str:
            for i in text:
                data += chr((ord(i) + self.shift) % self.chars)
            data_encoded = ''.join([format(ord(j), "08b") for j in data])
            return data_encoded
        else:
            print('Format error')
    
    # convert binary data into text
    # your code should be similar to the corresponding code used for Codec
    def decode(self, data):
        text = ''
        # your code goes here
        binary = []        
        for i in range(0,len(data),8):
            byte = data[i: i+8]
            if byte == self.encode(self.delimiter): # you need to find the correct binary form for the delimiter
                break
            binary.append(byte)
        text = ''
        for byte in binary:
            text += chr((int(byte,2)-self.shift) % self.chars)
        return text

# a helper class used for class HuffmanCodes that implements a Huffman tree
class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.left = left
        self.right = right
        self.freq = freq
        self.symbol = symbol
        self.code = ''
        
class HuffmanCodes(Codec):
    
    def __init__(self, delimiter='#'):
        self.nodes = None
        self.name = 'huffman'
        self.delimiter = delimiter

    # make a Huffman Tree    
    def make_tree(self, data):
        # make nodes
        nodes = [Node(freq, char) for char, freq in data.items()]
            
        # assemble the nodes into a tree
        while len(nodes) > 1:
            # sort the current nodes by frequency
            nodes = sorted(nodes, key=lambda x: x.freq)

            # pick two nodes with the lowest frequencies
            left = nodes.pop(0)
            right = nodes.pop(0)

            # combine the nodes into a tree
            combo = Node(left.freq+right.freq, left.symbol+right.symbol,
                        left, right)

            # assign codes
            left.code = '0'
            right.code = '1'

            # traverse the tree for the Huffman codes
            h_code = {}
            self.traverse_tree(combo, '', h_code)

            # remove the two nodes and add their parent to the list of nodes
            nodes.append(combo)
        
        root = nodes[0]
        h_code = {}
        self.traverse_tree(root, '', h_code)

        return root, h_code

    # traverse a Huffman tree
    def traverse_tree(self, node, val, h_code):
        next_val = val + node.code
        if(node.left):
            self.traverse_tree(node.left, next_val, h_code)
        if(node.right):
            self.traverse_tree(node.right, next_val, h_code)
        if(not node.left and not node.right):
            # print(f"{node.symbol}->{next_val}") # this is for debugging
            # you need to update this part of the code
            # or rearrange it so it suits your needs
            h_code[node.symbol] = next_val

    # convert text into binary form
    def encode(self, text):
        
        d = {letter: text.count(letter) for letter in set(text)}
        
        self.nodes, h_code = self.make_tree(d)

        data = ''.join(h_code[letter] for letter in text)
        return data

    # convert binary data into text
    def decode(self, data):
        text = ''
        # your code goes here
        curr = self.nodes
        # using data length we loop
        for i in range(len(data)):
            # if 0 is encountered we move to the left of tree
            if data[i] == '0':
                curr = curr.left
            # else move right
            else:
                curr = curr.right
            # if leaf then we add it to text (result) and set current curr equal to nodes (root)
            if (curr.left == None and curr.right == None):
                text += curr.symbol
                curr = self.nodes
            # stop processing if delimiter is encountered
            if text.endswith(self.delimiter):
                break
        # return the decoded text
        return text[:-len(self.delimiter)]


# driver program for codec classes
if __name__ == '__main__':
    text = 'hello' 
    #text = 'Casino Royale 10:30 Order martini' 
    print('Original:', text)
    
    c = Codec()
    binary = c.encode(text + c.delimiter)
    # NOTE: binary should have a delimiter and text should not have a delimiter
    print('Binary:', binary) # should print '011010000110010101101100011011000110111100100011'
    data = c.decode(binary)  
    print('Text:', data)     # should print 'hello'
    
    cc = CaesarCypher()
    binary = cc.encode(text + cc.delimiter)
    # NOTE: binary should have a delimiter and text should not have a delimiter
    print('Binary:', binary)
    data = cc.decode(binary) 
    print('Text:', data)     # should print 'hello'
     
    h = HuffmanCodes()
    binary = h.encode(text + h.delimiter)
    # NOTE: binary should have a delimiter and text should not have a delimiter
    print('Binary:', binary)
    data = h.decode(binary)
    print('Text:', data)     # should print 'hello'


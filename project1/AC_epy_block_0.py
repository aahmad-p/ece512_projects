"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import time
import collections


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, start_pattern=[0,1,0,1,0,0,1,1], payload_length=80):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.byte],#in_sig=[np.byte]
            out_sig=[np.byte]
        )
        
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.start_pattern = start_pattern
        self.start_pattern_length = len(start_pattern)
        
        self.payload_length = payload_length
        
        # Use a deque for an efficient fixed-size sliding window
        self.buffer = collections.deque(maxlen=self.start_pattern_length)
        
        self.morse = {
            18: "A",
            13: "B",
            26: "C",
            11: "D",
            28: "E",
            7: "F",
            22: "G",
            14: "H",
            25: "I",
            5: "Z",
            17: "K",
            9: "L",
            29: "M",
            6: "V",
            23: "O",
            12: "P",
            27: "Q",
            4: "R",
            19: "S",
            10: "T",
            30: "U",
            20: "W",
            15: "X",
            24: "Y",
            0: "?",
            21: " "
        }
        
        
    def work(self, input_items, output_items):
        # [0,1,0,1,0,0,1,1,0,1,0,0,1,0,0,0,0,1,1,0,0,1,0,1,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,1,1,0,0,1,0,0,0,0,1]
        # Start message ("S"): 0,1,0,1,0,0,1,1
        sleep_sec = 5
        
        data_in = input_items[0]
        #data_in = data_in[len(data_in)-70:len(data_in)]
        #print(self.start_pattern)
        #print(input_items[0][:])
        
        print("Processing ", len(input_items[0][:]), " bits")
        # Check if any element in the array is equal to the target value
        if len(input_items[0][:]) >= (self.start_pattern_length + self.payload_length):
            print("Looking for a message start sequence ...")
            
            #num_items_search = len(data_in) - (len(data_in) % self.payload_length)
            #data_in_search = data_in[0:num_items_search]
            data_in_search = data_in
            
            #print("Had ", len(data_in), " items. Searching through ", len(data_in_search), " items.")
            for index, item in enumerate(data_in_search):
                if (len(data_in_search) - index - 1) < self.payload_length:
                    break
                
                self.buffer.append(item)
                
                # Check for the start_pattern only when the buffer is full
                if len(self.buffer) == self.start_pattern_length:
                    if list(self.buffer) == self.start_pattern:
                        print("A message start sequence was found! Reading the message ...")
                        print(index)
                        print(len(data_in_search))
                        
                        
                        extracted_payload = data_in_search[(index + 1):(index + 1 + self.payload_length)]
                        extracted_payload_with_start = data_in_search[(index + 1 - self.start_pattern_length):(index + 1 + self.payload_length)]
                        #converted_chars = self.bits_to_chars(extracted_payload)
                        converted_chars = self.bits_to_custom_chars(extracted_payload)
                        print(extracted_payload_with_start)
                        print("".join(converted_chars).replace("?", "").replace("!",""))
                        #print(converted_chars)
                        
                        time.sleep(sleep_sec)
                        return len(output_items[0])

        time.sleep(sleep_sec)
        
        return len(output_items[0])
        
    def bits_to_custom_chars(self, bit_list):
        """
        Converts a list of 0s and 1s (bits) into a list of characters.
        Args: bit_list (list): A list of integers (0 or 1) representing a bit stream.
        Returns: List: A list of characters.
        """
        # Ensure the bit list length is a multiple of 5
        if len(bit_list) % 5 != 0:
            raise ValueError("The bit list must have a length that is a multiple of 5 to form custom characters.")
        
        custom_char_list = []
        # Process the bit stream in chunks of 5
        for i in range(0, len(bit_list), 5):
            custom_byte_value = 0
            five_bits = bit_list[i:i+5]
            #print(five_bits)
            
            # Convert the 5 bits to a single byte value
            for j in range(5):
                custom_byte_value += five_bits[j] * (2**((5-1) - j))
            
            #print(custom_byte_value)
            if not(custom_byte_value in self.morse):
                custom_char_list.append("!")
            else:
                # Convert the byte value to a character and add to the list
                custom_char_list.append(self.morse[custom_byte_value])
            
        return custom_char_list
    
    
    def bits_to_chars(self, bit_list):
        """
        Converts a list of 0s and 1s (bits) into a list of characters.
        Args: bit_list (list): A list of integers (0 or 1) representing a bit stream.
        Returns: List: A list of characters.
        """
        # Ensure the bit list length is a multiple of 8
        if len(bit_list) % 8 != 0:
            raise ValueError("The bit list must have a length that is a multiple of 8 to form characters.")
        
        char_list = []
        # Process the bit stream in chunks of 8
        for i in range(0, len(bit_list), 8):
            byte_value = 0
            eight_bits = bit_list[i:i+8]
            
            # Convert the 8 bits to a single byte value
            for j in range(8):
                byte_value += eight_bits[j] * (2**(7 - j))
                
            # Convert the byte value to a character and add to the list
            char_list.append(chr(byte_value))
            
        return char_list
        
        
    
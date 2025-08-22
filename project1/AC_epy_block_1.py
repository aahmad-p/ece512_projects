"""
Morse code vector source
"""

#  epy_block_0.py
#  revised 09/10/2019 - finish code table
#  revised 09/11/2019 - test for bad character
#  revised 09/27/2019 - get input from a Message Edit block (code from Volker Schroer dl1ksv)

import numpy as np
from gnuradio import gr

import pmt

textboxValue = ""

Morse = {
  # codes from https://www.itu.int/rec/R-REC-M.1677-1-200910-I/en
"A": "1,0,0,1,0",
  "B": "0,1,1,0,1",
  "C": "1,1,0,1,0",
  "D": "0,1,0,1,1",
  "E": "1,1,1,0,0",
  "F": "0,0,1,1,1",
  "G": "1,0,1,1,0",
  "H": "0,1,1,1,0",
  "I": "1,1,0,0,1",
  "J": "0,0,1,0,1",
  "K": "1,0,0,0,1", 
  "L": "0,1,0,0,1",
  "M": "1,1,1,0,1",
  "N": "0,0,1,1,0",
  "O": "1,0,1,1,1",
  "P": "0,1,1,0,0",
  "Q": "1,1,0,1,1",
  "R": "0,0,1,0,0",
  "S": "1,0,0,1,1",
  "T": "0,1,0,1,0",
  "U": "1,1,1,1,0",
  "V": "0,0,1,1,0",
  "W": "1,0,1,0,0",
  "X": "0,1,1,1,1",
  "Y": "1,1,0,0,0",
  "Z": "0,0,1,0,1",
  " ": "1,0,1,0,1",
  "?": "0,0,0,0,0",
      }

class mc_sync_block(gr.sync_block):
    """
    reads input from a message port
    generates a vector of Morse code bits
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name = "Morse code vector source",
            in_sig = None,
            out_sig = [np.byte])
        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('clear_input'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)

    def handle_msg(self, msg):
        global textboxValue
        textboxValue = pmt.symbol_to_string (msg)
        # print (textboxValue)
    
    def work(self, input_items, output_items):
        global Morse
        global textboxValue
        bit_stream = "1,1,0,1,1,1,0,1,0,1,0,1"
        if (len (textboxValue) > 0):
            for in0 in textboxValue:
                # get next char
                inChar = str (in0)
                # convert to upper case
                ch = inChar.upper()
                # test for character in table
                if (not(ch in Morse)):
                    print("bad char", ch)
                    ch = "?"        # replace bad character with a '?'
                # build vector
                _dots = str (Morse.get(ch))
                # print (ch, _dots)
                bit_stream += (","+_dots)    # letter space

            # bit_stream += ",0,0,0,0," + bit_stream # finish with word space
            bit_stream += ",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
            print (bit_stream)

            # get length of string
            _len = len(bit_stream)
            # num of elements = (length+1) / 2
            _num_elem = int((_len+1) / 2)
            print(_num_elem)

            # convert and store elements in output array
            for x in range (_len):
                y = int(x / 2)
                if (bit_stream[x] == '1'):
                    output_items[0][y] = 1
                elif (bit_stream[x] == '0'):
                    output_items[0][y] = 0
                else:
                    continue    # skip commas

            # clear input line
            textboxValue = ""
            # self.message_port_pub(pmt.intern('clear_input'), pmt.intern(''))
        else:
            _num_elem = 0

        return (_num_elem)
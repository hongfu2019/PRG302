"""
1. generate a random word from target.txt file saved in folder ./word-bank
2. print t_word 
"""
"""
flowchart
"""
# coding

import random as r
#path = "C:/Users/5004076/OneDrive - TAFE/PRG302/Week 10/word-bank/"
path = "./word-bank/"
t_filename = 'target_words.txt'
file_path_name = path + t_filename 

f_handler = open(file_path_name, 'r') # open the file

t_word = [] # t_word = list()

t_word = f_handler.read()
t_word = t_word.split() # copy all the strings from target_words into list
target_word = r.choice(t_word)

while True:
    input(" Press any key to continue ")
    target_word = r.choice(t_word)
    print(target_word) 

# testing using DocString 

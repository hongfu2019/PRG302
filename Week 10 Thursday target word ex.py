"""
1. read target file
2. generate a target word
3. print the target word

"""
"""
flowchart
"""
import random 
path = "C:/Users/5004076/OneDrive - TAFE/PRG302/Week 10/word-bank/" # path 
t_filename = 'target_words.txt' 
file_path_name = path + t_filename
file_handler = open(file_path_name, "r")
t_content = file_handler.read() # read target file content and store in a strings 
t_content_list = t_content.split() # convert string to list data structure

while True: 
    target_word = random.choice(t_content_list) # generate random word
    print(target_word)
    input("press enter to continue ...") 

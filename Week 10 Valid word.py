"""
1. check guess word is valid

"""
"""

"""
# coding
path = "./word-bank/"
w_filename = 'all_words.txt'
file_path_name = path + w_filename 

w_handler = open(file_path_name, 'r') # open the file

w_word = [] # t_word = list()

w_word = w_handler.read()
w_word = w_word.split() # copy all the strings from target_words into list


while True:
    v_guess = input(" Enter a valid guess word ")
    if v_guess in w_word:
        print(v_guess, " is valid")
    else:
        print(v_guess, " is NOT VALID")
    

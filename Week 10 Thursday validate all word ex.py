"""
1. read target file
2. generate a target word
3. print the target word

"""
"""
flowchart
"""

path = "./word-bank/" # path 
w_filename = 'all_words.txt' 
file_path_name = path + w_filename
file_handler = open(file_path_name, "r")
w_content = file_handler.read() # read target file content and store in a strings 
w_content_list = w_content.split() # convert string to list data structure

while True:
    guess_word = input(" Please enter guess word ")
    if guess_word in w_content_list:
        print(guess_word, " is VALID !!!")
    else:
        print(guess_word, " is NOT VALID")
    

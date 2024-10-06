"""
1. check guess word against target word
2. put a score ('2,'2','2','2,'2') (tuple) == all match 
"""
"""
flowchart
"""
# coding 
target_word = 'dance'
guess_word = 'dunce'
t_target = tuple(target_word)
t_guess = tuple(guess_word)

tuple_score = ()

for i in range(5):
    if t_guess[i] == t_target[i]:
        score = 2
    else:
        if t_guess[i] in t_target:
            score = 1
        else:
            score = 0

    tuple_score = tuple_score + tuple(str(score))
print(tuple_score) 

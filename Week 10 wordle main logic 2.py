"""
target = 'hello'
guess = 'hence'
"""
"""
flowchart
"""
target = 'hello'

guess = 'hence'

target_tuple = tuple(target)
guess_tuple = tuple(guess) 

score_tuple = () # score_tuple = tuple()
score = 0
for i in range(5):
    if guess_tuple[i] == target_tuple[i]:
        score = 2
    else:
        if guess_tuple[i] in target_tuple:
            score = 1
    score_tuple = score_tuple + tuple(str(score))
    score = 0

print(score_tuple) 

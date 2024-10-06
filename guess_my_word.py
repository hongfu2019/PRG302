#!/usr/bin/env python3
"""Guess-My-Word is a game where the player has to guess a word.
A player is given 6 guesses. Each guess is 'scored' by indicating:
each letter that is correct (letter and position); and each letter
that is present in the target word but not in the correct position.

Author: Tim Oliver
Company: TAFE
Copyright: 2024

"""
# Your code must use PEP8
# Your code must be compatible with Python 3.1x
# You cannot use any libraries outside the python standard library without the explicit permission of your lecturer.

# This code uses terms and symbols adopted from the following source:
# See https://github.com/3b1b/videos/blob/68ca9cfa8cf5a41c965b2015ec8aa5f2aa288f26/_2022/wordle/simulations.py#L104

import random
import datetime


MISS = 0  # _-.: letter not found ⬜
MISPLACED = 1  # O, ?: letter in wrong place 🟨
EXACT = 2  # X, +: right letter, right place 🟩

MAX_ATTEMPTS = 6
WORD_LENGTH = 5

ALL_WORDS = 'word-bank/all_words.txt'
TARGET_WORDS = 'word-bank/target_words.txt'

SCORE_FILE = 'scores.log'
EXIT_IO_ERROR = -1

# Stolen from https://www.nytimes.com/games/wordle/index.html
# Ask forgiveness not permission and all that
SUPERLATIVES = ['Genius',
                'Magnificent',
                'Impressive',
                'Splendid',
                'Great',
                'Phew']
ORDINALS = ['First',
            'Second',
            'Third',
            'Fourth',
            'Fifth',
            'Last']
cheat = True  # Set True to print target word for testing


def play():
    player_name = input("\nPlease tell me your name: ")
    # Log reading code will fail if player_name has a space, so remove any
    player_name = player_name.strip().replace(" ", "").replace("\t", "")
    if 0 == len(player_name):
        player_name = "Anonymous"
    print("\nWelcome to Wordle, " + player_name + ", shall we play a game?")
    help()
    # What follows is now  a mess... Could probably be turned into one
    # big fun switch statement with Enum for state?
    playtime_over = False
    valid_words = get_valid_words()
    score_log = []
    while not playtime_over:
        attempt = 0
        guesses = []
        game_won = False
        word_of_the_day = get_target_word()
        while attempt < MAX_ATTEMPTS:
            print(ORDINALS[attempt] + " try"
                  + ("\t" * 13 + "Target: " + word_of_the_day if cheat else ""))
            guess = ask_for_guess(valid_words)
            match guess:
                case "done":
                    print("\t\tThanks for playing")
                    playtime_over = True
                    break
                case "help":
                    help()
                    continue
                case _ if guess in valid_words:
                    guesses.append(guess)
                    score = score_guess(guess, word_of_the_day)
                    print("\nResult of your guess:"
                          + score_tabber(format_score(guess, score)))
                    if is_correct(score):
                        print("\n\t\t" + SUPERLATIVES[attempt] + "!\tYou guessed the word in "
                              + str(attempt + 1) + " attempt" + ("" if attempt == 0 else "s"))
                        game_won = True
                        break
                    attempt += 1
        if not playtime_over:
            # We are storing a date/time in non-UTC form without a timezone which is bad.
            timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            score_log.append((timestamp, player_name, word_of_the_day, guesses))
            print('The target word is ===>',word_of_the_day)
            if not game_won:
                print("\n\t\t\tSorry, you have no guesses left.\n"
                      "\t\t\tI'm guessing you do not play Scrabble. \U0001F61B")
        # print(score_log)
        if not playtime_over:
            if input("\n\t\tShall we play again? ").lower().startswith("y"):
                continue
        playtime_over = True
    post_game_stats(player_name, score_log)
    
    
def post_game_stats(player_name, score_log):
    # Append log entries
    if 0 < len(score_log):
        try:
            h = open(SCORE_FILE, "a")
            for game in score_log:
                output = (game[0] + " " + game[1]
                          + (" guessed " if game[2] == game[3][-1] else " failed to guess ")
                          + game[2] + " with guesses:")
                for word in game[3]:
                    output += " " + word
                output += "\n"
                h.write(output)
        except IOError:
            print(f"Error writing {SCORE_FILE}")
            exit(EXIT_IO_ERROR)
        h.close()
    # Session stats
    (games_won, games_played, guesses_total, won_game_guesses) = get_stats_from_log(score_log)
    if 0 < games_played:
        print(f"{player_name}, your statistics for this session are:")
        print(f"\tGames won/played\t\t\t\t\t{games_won} / {games_played}")
        if 0 < games_won:
            print(f"\tAverage guesses required to win:\t{won_game_guesses / games_won:.2f}")
    # Lifetime stats
    full_log = scan_scores_for_player(player_name)
    (games_won, games_played, guesses_total, won_game_guesses) = get_stats_from_log(full_log)
    if 0 < games_played:
        print(f"{player_name}, your lifetime statistics are:")
        print(f"\tGames won/played:\t\t\t\t\t{games_won} / {games_played}")
        if 0 < games_won:
            print(f"\tAverage guesses required to win:\t{won_game_guesses / games_won:.2f}")


def get_stats_from_log(log):
    games_won = 0
    games_played = 0
    guesses_total = 0
    won_game_guesses = 0
    for score in log:
        games_played += 1
        if score[2] == score[3][-1]:
            games_won += 1
            won_game_guesses += len(score[3])
        guesses_total += len(score[3])
    return games_won, games_played, guesses_total, won_game_guesses
    

def scan_scores_for_player(player_name):
    safe_name = player_name.strip()
    history = []
    fh = open(SCORE_FILE, "r")
    fulltext = fh.readlines()
    for line in fulltext:
        if line.split()[1].lower() != safe_name.lower():
            continue
        if "failed to guess":
            line = line.replace("failed to guess", "failed")
        line = line.replace("with guesses:", "")
        # Line should now be "<datetime> <player> [failed|guessed] <target> <words>+"
        words = line.split()
        guesses = []
        for i in range(4, len(words)):
            guesses.append(words[i])
        history.append(("NotUsed", words[1], words[3], guesses))
    fh.close()
    return history


def score_tabber(string):
    """Prepend each line of score_guess' output with tabs, to avoid
    messing with that functions docstring tests."""
    lines = string.split("\n", 1)
    tabbed_string = "\t"*2 + lines[0] + "\n"
    tabbed_string += "\t"*7 + lines[1]
    return tabbed_string


def is_correct(score):
    """Checks if the score is entirely correct and returns True if it is
    Examples:
    >>> is_correct((1,1,1,1,1))
    False
    >>> is_correct((2,2,2,2,1))
    False
    >>> is_correct((0,0,0,0,0))
    False
    >>> is_correct((2,2,2,2,2))
    True"""
    for pos in score:
        if pos is not EXACT:
            return False
    return True


def get_valid_words(file_path=ALL_WORDS):
    """returns a list containing all valid words.
    Note to test that the file is read correctly, use:
    >>> get_valid_words()[0]
    'aahed'
    >>> get_valid_words()[-1]
    'zymic'
    >>> get_valid_words()[10:15]
    ['abamp', 'aband', 'abase', 'abash', 'abask']
    """
    valid_words = list()
    try:
        fh = open(file_path)
    except OSError:
        print(f'Failed to open file: {file_path}')
        exit(-1)
    for word in fh:
        word = word.rstrip()
        assert len(word) == WORD_LENGTH, word
        valid_words.append(word)
    return valid_words


def get_target_word(file_path=TARGET_WORDS, seed=None):
    """Picks a random word from a file of words

    Args:
        file_path (str): the path to the file containing the words
        seed: random number seed
        
    Returns:
        str: a random word from the file

    How do you test that a random word chooser is choosing the correct words??
    Discuss in class!
    #>>> get_target_word()
    'aback'
    #>>> get_target_word()
    'zonal'
    """
    # read words from a file and return a random word (word of the day)
    target_words = get_valid_words(file_path)
    random.seed(seed)
    return random.choice(target_words)


def ask_for_guess(valid_words):
    """Requests a guess from the user directly from stdout/in
    Returns:
        str: the guess chosen by the user. Ensures guess is a valid word of correct length in lowercase
             or 'done' to exit, or 'help' for help
    """
    while True:
        guess = input('Enter your guess (or "help" or "done"): ')
        guess = guess.lower()
        if guess == 'done' or guess == 'help' or guess in valid_words:
            return guess
        print('That is not a five letter word that I know')


def score_guess(guess, target_word):
    """given two strings of equal length, returns a tuple of ints representing the score of the guess
    against the target word (MISS, MISPLACED, or EXACT)
    Here are some example (will run as doctest):

    >>> score_guess('hello', 'hello')
    (2, 2, 2, 2, 2)
    >>> score_guess('drain', 'float')
    (0, 0, 1, 0, 0)
    >>> score_guess('hello', 'spams')
    (0, 0, 0, 0, 0)

    Try and pass the first few tests in the doctest before passing these tests.
    >>> score_guess('gauge', 'range')
    (0, 2, 0, 2, 2)
    >>> score_guess('melee', 'erect')
    (0, 1, 0, 1, 0)
    >>> score_guess('array', 'spray')
    (0, 0, 2, 2, 2)
    >>> score_guess('train', 'tenor')
    (2, 1, 0, 0, 1)
    >>> score_guess('exeme', 'femme')
    (1, 0, 0, 2, 2)
    >>> score_guess('exeme', 'feese')
    (1, 0, 2, 0, 2)
    >>> score_guess('feese', 'exeme')
    (0, 1, 2, 0, 2)
    >>> score_guess('lllwh', 'whell')
    (1, 1, 0, 1, 1)
    """
    target = list(target_word)
    score = [MISS for _ in range(5)]
    
    for guess_pos in range(WORD_LENGTH):
        if guess[guess_pos] == target[guess_pos]:
            score[guess_pos] = EXACT
            target[guess_pos] = None
            # print(f'i{guess_pos} guess:{guess}, score:{score} target:{target}')
    for guess_pos in range(WORD_LENGTH):
        if score[guess_pos] == EXACT:
            continue
        for target_pos in range(WORD_LENGTH):
            # print(f'i{guess_pos} j{target_pos} guess:{guess}), score:{score} target:{target}')
            if guess[guess_pos] == target[target_pos]:
                score[guess_pos] = MISPLACED
                target[target_pos] = None
                # print(f'i{guess_pos} j{target_pos} guess:{guess}), score:{score} target:{target}')
                break
    return tuple(score)


def help():
    """Provides help for the game"""
    print("\n\tWordle is a find-the-word puzzle game where the player has \n"
          "\tsix guesses at the word. After each guess any letters \n"
          "\tin the correct position are marked with a '+' and any \n"
          "\tcorrect letters that are simply in the wrong position are \n"
          "\tmarked with a '?', the remaining letters are marked with\n"
          "\tas '_'. Each guess must be a valid word, (but dont worry, \n"
          "\tmy knowledge of five letter words is extensive).\n")


def format_score(guess, score):
    """Formats a guess with a given score as output to the terminal.
    The following is an example output (you can change it to meet your own creative ideas, 
    but be sure to update these examples)
    >>> print(format_score('hello', (0,0,0,0,0)))
    H E L L O
    _ _ _ _ _
    >>> print(format_score('hello', (0,0,0,1,1)))
    H E L L O
    _ _ _ ? ?
    >>> print(format_score('hello', (1,0,0,2,1)))
    H E L L O
    ? _ _ + ?
    >>> print(format_score('hello', (2,2,2,2,2)))
    H E L L O
    + + + + +"""

    sym_map = {MISS: '_', MISPLACED: '?', EXACT: '+'}
    # sym_map = '_', '?', '+'
    out = ''

    for g in guess:
        out += g.upper() + " "
    out = out[:-1]
    out += '\n'
    for s in score:
        out += sym_map[s] + " "
    out = out[:-1]
    # for i in range(len(guess)):
    #     out += guess[i].upper()
    #     if i < len(guess) - 1:
    #         out += ' '
    # out += '\n'
    # for i in range(len(score)):
    #     out += sym_map[score[i]]
    #     if i < len(score) - 1:
    #         out += ' '
    return out


def main(test=False):
    if test:
        import doctest
        return doctest.testmod()
    play()


if __name__ == '__main__':
    print(main(test=True))


main(False)

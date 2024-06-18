#this is basically a clone of the Wordle game that got like megapopular during the COVID lockdown.  
#except, instead of an library of almost 2300 five lettered words, we're only playing with about 50 six lettered words. 
#also the user can add new words to the list!

#program will check if new word is both six lettered and unique to the code, and not already in the list, before accepting it.

#this is to import the cool screen clearing thing. operating system agnostic, so HOPEFULLY should work when I submit this as my CiP4 capstone
import os

#this will import the "random" module, it is important to randomly pick a new word for each game
import random

#this will import the "time" module. it's needed for count downs.
import time

# Constants and Variables

#seperator for the boxes, so the game's grid looks nice!
separator = "-" * 50

#lives and chances player has. user can change this
starting_lives = 6

#default mode of lives, user cannot change this (immutable)
default_lives = 6

#time limit before game runs out, it does not update in real time unfortunatly. user can change this (modifiable)
time_limit_seconds = 300

#line to caluculate how many seconds in minutes, and another to reset to default to the original time limit.
time_limit_minutes = time_limit_seconds // 60
time_limit_seconds_default = 300

# List of words that random will pick from (user modifiable by adding new words)
word_list = [
    "growth", "notice", "orange", "unlike", "random", "choice", "scream",
    "relief", "absent", "banana", "depend", "winner", "strong", "muscle",
    "cancer", "battle", "lounge", "modest", "global", "annual", "mature",
    "treaty", "export", "asylum", "ignore", "topple", "damage", "cherry",
    "infect", "betray", "define", "dinner", "method", "detail", "figure",
    "symbol", "dragon", "bucket", "clique", "broken", "debate", "rabbit",
    "temple", "native", "cousin", "finish", "leader", "return", "horror",
    "basket"
]

# if i want to reset the words
default_word_list = word_list.copy()

# ANSI color codes for the grid. 
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RESET = '\033[0m'

#operating system clear screen. unsure if CiP4 would acceps
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_grid(guesses, remaining_time):
    timer_display = f"Time left: {remaining_time} seconds" #displays timer, and aligns it in grid //CHANGE THIS//
    timer_line = f"{' ':<12} {timer_display}"

    card = [separator, timer_line, separator] # Start building the grid

    # goes through each row in guesses
    for guess in guesses:
        #formats each user guess with borders and spaces
        card.append(f"|   {'   |   '.join(guess)}   |")
        card.append(separator) #seperates after row
    return "\n".join(card) # Join all parts with newlines to form the grid string

def generate_feedback(secret_word, guess):
    feedback = []
    for sw_char, guess_char in zip(secret_word, guess):
        if guess_char == sw_char:
            feedback.append(f"{GREEN}{guess_char.upper()}{RESET}")  # Correct letter in the correct place
        elif guess_char in secret_word:
            feedback.append(f"{YELLOW}{guess_char.lower()}{RESET}")  # Correct letter in the wrong place
        else:
            feedback.append(f"{RED}{guess_char}{RESET}")  # Incorrect letter
    return feedback

def timer():
    global time_limit_seconds
    global time_limit_minutes
    
    while True:
        question = input(f"Current time limit: {time_limit_minutes} minutes, type a new limit (seconds) to change this (between 60 to 3599). Enter 'RESET' to reset timer. Anything else to quit:\n").strip().lower()
        
        if question == "reset":
            time_limit_seconds = time_limit_seconds_default
            time_limit_minutes = time_limit_seconds // 60
            print(f"Timer reset to default: {time_limit_minutes} minutes")
            time.sleep(1)
            main_menu()
        
        elif question.isdigit():
            new_timer = int(question)
            
            if new_timer < 60:
                clear_screen()
                print("Too low, try again.")
                
            elif new_timer > 3599:
                clear_screen()
                print("Too high, try again.")
                
            else:
                time_limit_seconds = new_timer
                time_limit_minutes = time_limit_seconds // 60
                print(f"Time limit changed to: {time_limit_minutes} minutes")
                time.sleep(1)
                main_menu()
        
        else:
            return

def settings(starting_lives, word_list, default_word_list, default_lives):
    clear_screen()    
    choice = input(f"1. Change Number of Guesses. Currently: {starting_lives}\n2. Reset Lives\n3. Reset Dictionary\n4. Return To Menu\n\nAnything Else To Quit Program\n\nChoose:")

    if choice == '1':
        new_number_of_lives = int(input("New Number Of Guesses: "))
        starting_lives = new_number_of_lives
        settings(starting_lives, word_list, default_word_list, default_lives)
    
    elif choice == '2':
        starting_lives = default_lives

    elif choice == '3':
        word_list[:] = default_word_list

    elif choice == '4':
        clear_screen()
        main_menu()    

def display_word_list_dictionary(word_list, default_word_list):
    while True:
        display_word_list(word_list)
        new_word_add = input("\nType a new word to add (must be six letters long).\nType 'reset' to reset the dictionary.\nType 'quit' to return to the menu.\n").strip().lower()

        if new_word_add == "quit":
            clear_screen()
            main_menu()
            break  

        elif new_word_add == "reset":
            clear_screen()
            word_list[:] = default_word_list[:]  

        elif len(new_word_add) != 6 or new_word_add in word_list:
            pass

        else:
            clear_screen()
            word_list.append(new_word_add)

def display_word_list(word_list):
    clear_screen()
    print("Current word list:")
    columns = 5  
    for i in range(0, len(word_list), columns):
        for word in word_list[i:i + columns]:
            print(f"{word:<10}", end=" ")  
        print()  

def changing_lives():
    global starting_lives
    global default_lives
    while True:
        question = input(f"Current lives: {starting_lives}, type a new number to change this (between 2 to 12). Enter 'RESET' to reset lives. Anything else to quit:\n").strip().lower()
        if question == "reset":
            starting_lives = default_lives
            print(f"Lives reset to default: {default_lives}")
            time.sleep(1)
            main_menu()
        elif question.isdigit():
            new_lives = int(question)
            if new_lives < 2:
                clear_screen()
                print("Too low, try again.")
            elif new_lives > 12:
                clear_screen()
                print("Too high, try again.")
            else:
                starting_lives = new_lives
                print(f"Lives changed to: {starting_lives}")
                time.sleep(1)
                main_menu()
        else:
            return

#main menu, first thing the user sees
def main_menu():
    clear_screen()
    print("Welcome to WORDLE - Python Edition!\n") 
    choice = input(f"1. Play Game\n2. Dictionary\n3. Change Lives. Current Lives: {starting_lives}\n4. Change Timer. Current Time Limit: {time_limit_minutes} minutes\n\nChoose: ") 

    if choice == "1": 
        play_game(starting_lives, word_list)

    elif choice == "2":
        display_word_list_dictionary(word_list, default_word_list)

    elif choice == "3":
        clear_screen()
        changing_lives()

    elif choice == "4":
        clear_screen()
        timer()

def play_game(starting_lives, word_list):
    clear_screen()
    secret_word = random.choice(word_list)  # Select a random word from the word list
    lives = starting_lives  # Set the number of lives to starting lives

    # Debug print statements
    print(f"debug: {secret_word}")
    print(f"debug: {lives}")

    # Initialize an empty grid of guesses
    guesses = [[" " for _ in range(6)] for _ in range(lives)]  
    start_time = time.time()  # Record the start time of the game
    attempt = 0  # Initialize attempt counter

    # Set to keep track of guessed words
    guessed_words = set()

    while attempt < lives:
        remaining_time = max(0, time_limit_seconds - int(time.time() - start_time))  # Calculate remaining time
        time_limit_minutes = time_limit_seconds // 60  # Update time_limit_minutes based on time_limit_seconds
        
        clear_screen()
        print(display_grid(guesses, remaining_time))  # Print the grid only once at the beginning of each attempt

        guess = input("Enter your guess: ").strip().lower()
        
        # Check if the guess has already been guessed before
        if guess in guessed_words:
            print("You've already guessed this word. Try a different one.")
            time.sleep(1)
            continue
        
        # Add the guess to the set of guessed words
        guessed_words.add(guess)

        # Validate the guess
        if len(guess) != 6 or not guess.isalpha():
            print("Invalid guess. Please enter a 6-letter word.")
            time.sleep(1)
            continue

        feedback = generate_feedback(secret_word, guess)
        guesses[attempt] = feedback
        attempt += 1

        if guess == secret_word:
            print("Congratulations! You've guessed the word!")
            time.sleep(5)
            main_menu()
        elif remaining_time <= 0:
            print(f"Time's up! The word was '{secret_word}'. Better luck next time!")
            time.sleep(5)
            main_menu()

    else:
        print(f"Out of lives! The word was '{secret_word}'. Better luck next time!")
        time.sleep(5)
        main_menu()

main_menu()

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here

    global secret_number
    secret_number = random.randrange(0, 100)
    
    global remain_guess
    remain_guess = math.ceil(math.log(100, 2))
    
    print "New game, Range is from 0 to 100"
    print "Remain number of guesses: " + str(int(remain_guess))

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     

    global secret_number
    secret_number = random.randrange(0, 1000)
    
    global remain_guess
    remain_guess = math.ceil(math.log(1000, 2))
    
    print "New game. Range is from 0 to 1000"
    print "Remain number of guesses: " + str(int(remain_guess))
    
    
def input_guess(guess):
    # main game logic goes here	
    
    print "\n"
    
    print "Guess was " + guess
    guess_num = int(guess)
    global remain_guess
    remain_guess -= 1    

    if (guess_num > secret_number) and (remain_guess > 0):
        print "Try a lower number"
        print "Remain number of guesses: " + str(int(remain_guess))
    elif (guess_num < secret_number) and (remain_guess > 0):
        print "Try a higher number"
        print "Remain number of guesses: " + str(int(remain_guess))
    elif (guess_num == secret_number) and (remain_guess >= 0):
        print "Correct" + "\n"
        # Correct guess, restart the game with the same range
        if secret_number > 100:
            range1000()
        else:
            range100()
    elif remain_guess == 0:
        print "Out of guesses, the number was " + str(secret_number) + "\n"
        # Out of guesses, restart the game with the same range
        if secret_number > 100:
            range1000()
        else:
            range100()
        
    

    
# create frame
frame = simplegui.create_frame('Guess the number', 300, 300)

# register event handlers for control elements and start frame

button1 = frame.add_button('Range is [0,100)', range100, 150)
button2 = frame.add_button('Range is [0,1000)' , range1000, 150)

enter1 = frame.add_input("Input the guess", input_guess, 100)

# call new_game 
new_game()

frame.start()

# always remember to check your completed program against the grading rubric

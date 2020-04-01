###################################################################
# Guessing Game. Input a word and have the player try to guess it #
###################################################################

# Assign a word to guess.

word = "stick"

# Begin Game
# Declare the amount of guesses with guess_limit.

print("All words are lower case, enter all guesses as lower case")

guess = ""
guess_count = 0
guess_limit = 4
out_of_guesses = False

# Create a while loop to test if the input matches the word. If input does not match the word, give a hint.
# guess_count increases by one after every guess. If guess_count reaches the guess_limit then the player is
# out of guesses and loses.

while guess != word and not out_of_guesses:
    if guess_count < guess_limit:
        guess = input("Enter Guess: ").lower().strip()
        guess_count += 1
        if guess_count == 1:
            print("The word is " + str((len(word))) + " letters.")
        elif guess_count == 2:
            print("The 2nd letter is " + str((word[1])) + ".")
        elif guess_count == 3:
            print("The 3rd letter is " + str((word[2])) + ".")
    else:
        out_of_guesses = True

if out_of_guesses:
    print("Out of Guesses, YOU LOSE! The word was " + word + ".")
else:
    print("You win!")

# End of program #

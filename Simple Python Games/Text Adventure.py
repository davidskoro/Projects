#######################################################################################
# Text Adventure Game. A short Text Adventure with user input that can restart itself #
#######################################################################################

# Define restart function.
# Declare the retry variable.
# If yes, restart. If no thank the user.


def restart():
    retry = input("Would you like to play again? (yes/no) ")
    if retry.lower().strip() == "yes":
        text_game()
    else:
        print("Thank you for playing")

# Define the text_game function.
# Receive input from the user. Depending on input print result.
# When game ends, call the restart function and allow the user to play again.


def text_game():
    print("Hello, welcome to the game")
    answer = input("Everything is dark, do you choose to wake up? (yes/no) ").lower().strip()
    if answer.lower().strip() == "yes":
        answer = input("You wake up on a rough bed in a stone room, what do you do? ").lower().strip()
        if answer == "look for a door":
            print("You escape. The End.")
            restart()
        elif answer == "look for an exit":
            print("You escape. The End.")
            restart()
        elif answer == "try to escape":
            print("You escape. The End.")
            restart()
        elif answer == "run":
            print("You run into a wall and give yourself a concussion that you never wake up from. The End. ")
            restart()
        elif answer == "call 911":
            print("You are saved! The End.")
            restart()
        elif answer == "cry":
            print("A monster enters but decides to comfort you. You become best friends. The End.")
            restart()
        elif answer == "investigate":
            answer = input("You find a secret hatch under your bed, do you open it? (yes/no)").lower().strip()
            if answer == "yes":
                print("You find a secret tunnel and escape. The End.")
                restart()
            elif answer == "no":
                print("A monster enters and kills you. The End")
                restart()
        else:
            print("A monster enters and kills you. The End.")
            retry = input("Would you like to play again? (yes/no) ")
            if retry.lower().strip() == "yes":
                text_game()
    elif answer.lower().strip() == "no":
        print("You sleep forever. The End.")
        restart()
    else:
        print("You cant seem to move your body and die. The End.")
        restart()


# Call the text_game function to run the game.


text_game()


# End of program.

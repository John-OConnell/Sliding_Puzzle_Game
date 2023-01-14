'''
    John O'Connell
    CS5001
    Fall 2021
    Final Project
    Main Driver for the CS5001 Puzzle Slide Game
'''

from game import *
import turtle

def main():

    # sets up the game window
    screen_setup()
    # runs the splash screen to start the game
    splash_screen()
    # gets name and number of moves from user
    player_name, max_moves = get_user_input()
    # creates the gameboard frame
    create_gameboard()
    # process' the puzzle selection, mario puzzle to start
    current_puzz = process_selection('mario.puz', player_name, max_moves)
    # runs the game ui
    run_game_ui(current_puzz)

if __name__ == "__main__":
    main()

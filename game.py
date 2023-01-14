'''
    John O'Connell
    CS5001
    Fall 2021
    Final Project
    Functions for the execution of the CS5001 Puzzle Slide Game
'''

import turtle
import random
import time
import os
from datetime import datetime
from math import sqrt
from puzz import Puzz

# sets amount of scramble moves puzzle makes to begin
SCRAMBLE_DIFFICULTY = 100

def draw_rec(turtle, base, height):
    '''
    Function -- draw_rec
        Draws a rectangle of input base and height using an input turtle from
        the python turtle module
    Parameters:
        turtle (turtle) -- turtle object from python's turtle module
        base (int) -- base length of the rectangle
        height (int) -- height of the rectangle
    Draws a rectangle in the turtle module. Returns None.
    '''
    for i in range(2):
        turtle.forward(base)
        turtle.right(90)
        turtle.forward(height)
        turtle.right(90)

def screen_setup():
    '''
    Function -- screen_setup
        Creates a screen for the Puzzle Slide game
    No Given Parameters
    Creates the Puzzle Slide game screen. Returns None.
    '''
    # add all resource images to the screen
    # creates a global screen to avoid passing screen into many functions
    global wn
    wn = turtle.Screen()
    for shape in os.listdir('Resources'):
        wn.addshape(f'Resources/{shape}')
    wn.title("CS5001 Sliding Puzzle Game")
    wn.screensize(800, 650)
    wn.setup(width = 850, height = 700)
    
def splash_screen():
    '''
    Function -- splash_screen
        Runs the splash screen for the Puzzle Slide game
    No Given Parameters
    Displays the splash screen for 4 seconds. Returns None.
    '''
    wn.bgpic('Resources/splash_screen.gif')
    wn.update()
    time.sleep(4)
    wn.clear()

def get_user_input():
    '''
    Function -- get_user_input
        Gets the users name and max number of moves in the Puzzle Slide game
    No Given Parameters
    Returns the users name and max number of moves.
    '''    
    player_name = wn.textinput("CS5001 Puzzle Slide", "Enter your name:")
    max_moves = int(wn.numinput("CS5001 Puzzle Slide",
                             "Enter the number of moves (chances) you want "\
                             "(5-200)?", minval=5, maxval=200))
    return player_name, max_moves

def create_gameboard():
    '''
    Function -- create_gameboard
        Creates the gameboard frame for the Puzzle Slide game. Also writes the
        leaderboard if leaderboard file is present.
    No Given Parameters
    Creates the frame and leaderboard for the Puzzle Slide game. Returns None.
    '''
    tr = turtle.Turtle()
    tr.ht()
    tr.up()
    tr.speed(0)
    tr.width(6)

    # draws game area rectangle
    tr.goto(-375, 300)
    tr.down()
    draw_rec(tr, 475, 475)
    tr.up()

    # draws button rectangle
    tr.goto(-375, -210)
    tr.down()
    draw_rec(tr, 750, 90)
    tr.up()

    # draws leaderboard rectangle
    tr.goto(125, 300)
    tr.width(5)
    tr.color('blue')
    tr.down()
    draw_rec(tr, 250, 475)
    tr.up()

    # writes leaderboard
    tr.goto(135, 265)
    tr.write('Leaders:', font=("Arial", 24, "bold"))
    tr.goto(140, 240)
    
    # try/except block to check if leaderboard file is present
    try:
        with open('leaderboard.txt', mode='r') as leaderboard:
            leaderboard.readline()
            leaderboard.readline()
            leaders = leaderboard.readlines()
            for i in range(len(leaders)):
                leaders[i] = leaders[i].strip()
                leaders[i] = leaders[i].split('\t')
        for i in range(len(leaders)):
            tr.write(str(i+1) + ') ' + leaders[i][0] + ' : ' + leaders[i][1],
                     font=("Arial", 16, "normal"))
            tr.right(90)
            tr.forward(30)
            tr.left(90)
            
    except FileNotFoundError:
        error_logger('Leaderboard Error')
        tr.home()
        tr.shape('Resources/leaderboard_error.gif')
        tr.st()
        time.sleep(4)
        tr.ht()
        tr.shape('classic')
        
    # writes player moves line
    tr.color('black')
    tr.goto(-325, -270)
    tr.write('Player Moves: ', font=("Arial", 24, "bold"))

def process_selection(puzzle, player_name, max_moves):
    '''
    Function -- process_selection
        Process' user puzzle selection in the Puzzle Slide game. Creates an
        instance of the puzz class given the user inputs.
    Parameters:
        puzzle (str) -- name of the puzzle to process
        player_name (str) -- name of the player
        max_moves (int) -- maximum number of moves chosen by the player
    Process' user puzzle selection. Creates an instance of the puzz class
    with necessary variables. Returns the instance of the puz class created.
    '''
    # open selected .puz file
    with open(puzzle, mode='r') as puz_file:
        # get puzzle name
        name = puz_file.readline()
        name = name.split()
        name = name[1]

        # get number of puzzle pieces
        number = puz_file.readline()
        number = number.split()
        number = int(number[1])

        # calculate board size number
        square_num = int(sqrt(number))

        # get size of each tile
        size = puz_file.readline()
        size = size.split()
        size = int(size[1])

        # get thumbnail image file name
        thumbnail = puz_file.readline()
        thumbnail = thumbnail.split()
        thumbnail = thumbnail[1]

        # get tile image file names
        images = puz_file.readlines()
        for i in range(len(images)):
            images[i] = images[i].split()
            images[i][0] = int(images[i][0].strip(':'))
                
        # sort tile images by associated numer in .puzz file    
        images = sorted(images, key=lambda x: x[0])

    # add all necessary images to the screen
    for i in range(len(images)):
        wn.addshape(images[i][1])

    # return an instance of the puzz class
    return Puzz(player_name, name, number, square_num, size, thumbnail,
                images, max_moves)

def run_game_ui(puzz):
    '''
    Function -- run_game_ui
        Runs the user interface for the Puzzle Slide game.
    Parameters:
        puzz (puzz) -- an instance of the puzz class
    Runs the user interface for the Puzzle Slide game including registering
    all screen clicks. Returns None.
    '''
    # create nested list to represent game board
    board = [['tile' for i in range(puzz.square_num)] \
             for j in range(puzz.square_num)]
    
    # pen for creating tile outlines
    board_pen = turtle.Turtle()
    board_pen.ht()
    board_pen.speed(0)
    board_pen.up()

    # pen for counting moves
    move_pen = turtle.Turtle()
    move_pen.ht()
    move_pen.speed(0)
    move_pen.up()
    move_pen.goto(-155, -270)

    # turtle for displaying thumbnail image
    tn = turtle.Turtle()
    tn.ht()
    tn.up()

    # check if puzz.thumbnail in os.listdir():
    if os.path.exists(puzz.thumbnail):
        wn.addshape(puzz.thumbnail)
        tn.shape(puzz.thumbnail)
        tn.goto(315, 275)
        tn.st()
    # if thumbnail file doesn't exist, log the error
    else:
        error_logger('Thumbnail Error', puzz.thumbnail)

    # create turtle instances for each image in the puzzle board
    for i in range(puzz.square_num):
        for j in range(puzz.square_num):

            tile_num = puzz.square_num * i + j
            tile = turtle.Turtle()
            tile.ht()
            tile.shape(puzz.images[tile_num][1])
            tile.speed(0)
            tile.up()
            board[i][j] = tile

            # function for handling tile clicks
            def click_handler(x, y, tile=tile, board=board):
                '''
                    Function -- click handler
                        Handle clicks on the puzzle board
                    Parameters:
                        x (int) -- x coordinate of the turtle clicked
                        y (int) -- y coordinate of the turtle clicked
                        tile (turtle) -- the turtle that was clicked
                        board (lst) -- nested list representing the game board
                    Registers clicks on the game board and swaps tiles if
                    appropriate. Returns None.
                '''
                # updates move count only if tiles were swapped
                if swap_tile(tile, puzz, board):
                    puzz.moves += 1
                    move_pen.clear()
                    move_pen.write(f'{puzz.moves} / {puzz.max_moves}',
                               font=("Arial", 24, "bold"))
                    
                    # checks winning conditions and ends game if appropriate
                    if puzz.moves >= puzz.max_moves and not \
                       is_winner(puzz, board):
                        loss_screen()
                    elif is_winner(puzz, board):
                        update_leaderboard(puzz)
                        win_screen()
                        
            # passes click on a turtle into click_handler function
            tile.onclick(click_handler)

    # creates gameboard buttons
    create_buttons(puzz, board, board_pen, move_pen, tn)

    # scrambles board in a solvable manner
    scramble_board(puzz, board)

    # draws game board on the screen
    draw_board(puzz, board, board_pen)
      
def swap_tile(tile, puzz, board):
    '''
    Function -- swap_tiles
        Swaps tiles on the Puzzle Slide game gameboard if appropriate
    Parameters:
        tile (turtle) -- the turtle that was clicked on the gameboard
        puzz (puzz) -- an instance of the puzz class
        board (lst) -- nested list representing the game board
    Swaps tiles on the gameboard and in the representative board list only
    if tile is adjacent to blank tile. Returns True if the swap was succesful
    and False if it was not.
    '''
    # get coordinates of clicked on tile
    tile_x, tile_y = tile.xcor(), tile.ycor()
    # get coordinates of blank tile
    blank_tile, blank_x, blank_y = find_blank_tile(puzz, board)

    # checks if clicked on tile is adjacent to blank tile
    if is_adjacent(puzz, tile_x, tile_y, blank_x, blank_y):
        tile_loc = get_nested_loc(board, tile)
        blank_loc = get_nested_loc(board, blank_tile)
        # tuple substitution to swap tiles in board list
        board[tile_loc[0]][tile_loc[1]], board[blank_loc[0]][blank_loc[1]] = \
        board[blank_loc[0]][blank_loc[1]], board[tile_loc[0]][tile_loc[1]]

        # move turtles on the game board
        tile.goto(blank_x, blank_y)
        blank_tile.goto(tile_x, tile_y)
        return True
    else:
        return False

def is_adjacent(puzz, tile1_x, tile1_y, tile2_x, tile2_y):
    '''
    Function -- is_adjacent
        Checks whether or not two tiles are adjacent in the Puzzle Slide
        game
    Parameters:
        puzz (puzz) -- an instance of the puzz class
        tile1_x (int) -- x coordinate of the first tile
        tile1_y (int) -- y coordinate of the first tile
        tile2_x (int) -- x coordinate of the second tile
        tile2_y (int) -- y coordinate of the second tile
    Returns True if the two tiles are adjacent and False if they are not.
    '''
    if tile1_x == tile2_x and abs(tile1_y - tile2_y) == puzz.size + 3:
        return True
    elif tile1_y == tile2_y and abs(tile1_x - tile2_x) == puzz.size + 3:
        return True
    else:
        return False

def find_blank_tile(puzz, board):
    '''
    Function -- find_blank_tile
        Finds the location of the blank tile in the Puzzle Slide game.
    Parameters:
        puzz (puzz) -- an instance of the puzz class
        board (lst) -- nested list representing the game board
    Returns the turtle instance that holds the blank tile as well as the
    x and y coordinate of the blank tile on the board.
    '''
    for row in board:
        for tile in row:
            if tile.shape() == f'Images/{puzz.name}/blank.gif':
                return tile, tile.xcor(), tile.ycor()

def get_nested_loc(nested_list, tile):
    '''
    Function -- get_nested_loc
        Finds the location of an object within a nested list.
    Parameters:
        nested_list (lst) -- nested list in which to search for the object
        tile () -- object to be found in the nested list. Can be various
                    data types
    Returns a tuple of the index position of the object in the nested list
    '''
    for sub_list in nested_list:
        if tile in sub_list:
            return nested_list.index(sub_list), sub_list.index(tile)

def create_buttons(puzz, board, board_pen, move_pen, tn):
    '''
    Function -- create_buttons
        Creates all buttons in the Puzzle Slide game. Registers clicks and
        runs the associated function for all buttons
    Parameters:
        puzz (puzz) -- an instance of the puzz class
        board (lst) -- nested list representing the game board
        board_pen (turtle) -- instance of the turtle class used to draw board
        move_pen (turtle) -- instance of the turtle class used to update move
                                count
        tn (turtle) -- instance of the turtle class used to display thumbnail
    Creates all buttons on the game board, registers clicks on each button and
    runs the appropriate function for each button when clicked.
    '''
    def quit_func(x, y):
        '''
        Function -- quit_func
            Quits the Puzzle Slide game when the Quit button is clicked.
        Parameters:
            x (int) -- x coordinate of quit button
            y (int) -- y coordinate of quit button
        Quits the Puzzle Slide game. Returns None.
        '''
        qt = turtle.Turtle()
        qt.shape('Resources/quitmsg.gif')
        time.sleep(4)
        wn.clear()
        ct = turtle.Turtle().shape('Resources/credits.gif')
        time.sleep(8)
        quit()

    def load_func(x, y):
        '''
        Function -- load_func
            Get user input and loads a new puzzle in the Puzzle Slide game
            based on user input
        Parameters:
            x (int) -- x coordinate of load button
            y (int) -- y coordinate of load button
        Loads the user input puzzle in the Puzzle Slide game. Returns None.
        '''
        files = os.listdir()
        puz_files = ""
        for file in files:
            if file.endswith('.puz'):
                puz_files += f"{file}\n"
        selection = wn.textinput("CS5001 Puzzle Slide",\
                                 "Enter the name of the puzzle you wish to"\
                                 f" load. Choices are: \n{puz_files}")
        # checks whether user input is a valid puzzle choice
        if good_selection(selection):
            max_moves = int(wn.numinput("CS5001 Puzzle Slide",
                                        "Enter the number of moves (chances)"\
                                        " you want (5-200)?",
                                        minval=5, maxval=200))
        
            board_pen.clear()
            for inner_list in board:
                for tile in inner_list:
                    tile.ht()
            tn.ht()
            move_pen.clear()
            current_puzz = process_selection(selection, puzz.player_name,
                                         max_moves)
            run_game_ui(current_puzz)
            
        # if not a valid puzzle choice, reutrns to game
        else:
            return
        
    def reset_func(x, y):
        '''
        Function -- reset_func
            Resets the puzzle in the Puzzle Slide game
        Parameters:
            x (int) -- x coordinate of reset button
            y (int) -- y coordinate of reset button
        Redraws the puzzle in the solved position in the Puzzle Slide game.
        Returns none.
        '''
        tile_num = 0
        for row in board:
            for tile in row:
                tile.shape(puzz.images[tile_num][1])
                tile_num += 1
                
    # creates reset button    
    b1 = turtle.Turtle()
    b1.ht()
    b1.up()
    b1.speed(0)
    b1.shape('Resources/resetbutton.gif')
    b1.goto(145, -255)

    # creates load button 
    b2 = turtle.Turtle()
    b2.ht()
    b2.up()
    b2.speed(0)
    b2.shape('Resources/loadbutton.gif')
    b2.goto(235, -255)

    # creates quit button 
    b3 = turtle.Turtle()
    b3.ht()
    b3.up()
    b3.speed(0)
    b3.shape('Resources/quitbutton.gif')
    b3.goto(325, -255)

    # shows all buttons and registers clicks on each button 
    b3.st()
    b3.onclick(quit_func)
    b2.st()
    b2.onclick(load_func)
    b1.st()
    b1.onclick(reset_func)

def is_winner(puzz, board):
    '''
    Function -- is_winner
        Checks if the user wins in the Slide Puzzle game
    Parameters:
        puzz (puzz) -- an instance of the puzz class
        board (lst) -- nested list representing the game board
    Compares the nested list representing the game board to the solved image
    list to see if the puzzle is in the winning position. Returns True if the
    user has won and False if they have not.
    '''
    # compares shape of each tile in the puzzle to the ordered images list to
    # see if they match. (If they all match, the puzzle is in the winning
    # position)
    for i in range(puzz.square_num):
        for j in range(puzz.square_num):
            if board[i][j].shape() != \
                   puzz.images[puzz.square_num * i + j][1]:
                return False
    return True

def loss_screen():
    '''
    Function -- loss_screen
        Runs the loss screen in the Puzzle Slide game
    No Given Parameters
    Runs the loss screen in the Puzzle Slide game, shows the credits then
    quits the game. Returns None.
    '''
    lt = turtle.Turtle()
    lt.shape('Resources/Lose.gif')
    time.sleep(4)
    wn.clear()
    ct = turtle.Turtle().shape('Resources/credits.gif')
    time.sleep(8)
    quit()
    
def win_screen():
    '''
    Function -- win_screen
        Runs the win screen in the Puzzle Slide game
    No Given Parameters
    Runs the win screen in the Puzzle Slide game, shows the credits then
    quits the game. Returns None.
    '''
    wt = turtle.Turtle()
    wt.shape('Resources/winner.gif')
    time.sleep(4)
    wn.clear()
    ct = turtle.Turtle().shape('Resources/credits.gif')
    time.sleep(8)
    quit()
    
def scramble_board(puzz, board):
    '''
    Function -- scrabmble_board
        Scrables the game board in a solveable manner
    Parameters:
        puzz (puzz) -- an instance of the puzz class
        board (lst) -- nested list representing the game board
    Randomly moves the blank tile in the puzzle a predetermined number of times
    based on the set scramble difficutly. Returns None.
    '''
    # scrambles the board a predetermined number of times
    for i in range(SCRAMBLE_DIFFICULTY):
        blank_tile, blank_x, blank_y = find_blank_tile(puzz, board)
        blank_loc = get_nested_loc(board, blank_tile)
        directions = ["up", "down", "left", "right"]

        # removes directions that would cause an invalid puzzle
        if blank_loc[0] == 0:
            directions.remove("up")
        elif blank_loc[0] >= puzz.square_num - 1:
            directions.remove("down")
        if blank_loc[1] == 0:
            directions.remove("left")
        elif blank_loc[1] >= puzz.square_num - 1:
            directions.remove("right")

        direction = random.choice(directions)

        # moves blank tile in randomly selected direction
        if direction == "up":
            board[blank_loc[0] - 1][blank_loc[1]], \
                               board[blank_loc[0]][blank_loc[1]] = \
                               board[blank_loc[0]][blank_loc[1]], \
                               board[blank_loc[0] - 1][blank_loc[1]]
        if direction == "down":
            board[blank_loc[0] + 1][blank_loc[1]], \
                               board[blank_loc[0]][blank_loc[1]] = \
                               board[blank_loc[0]][blank_loc[1]], \
                               board[blank_loc[0] + 1][blank_loc[1]]

        if direction == "left":
            board[blank_loc[0]][blank_loc[1] - 1], \
                               board[blank_loc[0]][blank_loc[1]] = \
                               board[blank_loc[0]][blank_loc[1]], \
                               board[blank_loc[0]][blank_loc[1] - 1]

        if direction == "right":
            board[blank_loc[0]][blank_loc[1] + 1], \
                               board[blank_loc[0]][blank_loc[1]] = \
                               board[blank_loc[0]][blank_loc[1]], \
                               board[blank_loc[0]][blank_loc[1] + 1]
            
def draw_board(puzz, board, board_pen):
    '''
    Function -- draw_board
        Creates the board in the Puzzle Slide game
    Parameters:
        puzz (puzz) -- an instance of the puzz class
        board (lst) -- nested list representing the game board
        board_pen (turtle) -- instance of the turtle class used to draw board
    Creates the game board. Returns None.
    '''
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j].goto(-375 + ((puzz.size / 2) + 5) + \
                             j * (puzz.size + 3),
                             300 - ((puzz.size / 2) + 5) - \
                             i * (puzz.size + 3))
            board_pen.goto((-375 + 4) + j * (puzz.size + 3),
                           (300 - 4) - i * (puzz.size + 3))
            board_pen.down()
            draw_rec(board_pen, puzz.size + 1, puzz.size + 1)
            board_pen.up()
            board[i][j].st()
            
def good_selection(selection):
    '''
    Function -- good_selection
        Checks if the user selected puzzle in the Puzzle Slide game is valid
    Parameters:
        selection (str) -- the user input name of the puzzle file to validate
    Checks that all parameters of the selected puzzle are valid. Returns True
    if they are and False if they are not.
    '''
    # checks that selected puzzle file exists
    if selection not in os.listdir():
        error_logger('File Error', selection)
        puzz_error = turtle.Turtle()
        puzz_error.shape('Resources/file_error.gif')
        time.sleep(4)
        puzz_error.ht()
        return False
    # reads selected file to get necessary puzzle information
    with open(selection, mode='r') as puz_file:
        # skip puzzle name line
        name = puz_file.readline()
        # get number of puzzle pieces
        number = puz_file.readline()
        number = number.split()
        number = int(number[1])
        # get size of each tile
        size = puz_file.readline()
        size = size.split()
        size = int(size[1])
        # skip thumbnail file line
        thumbnail = puz_file.readline()
        # get tile image file names
        images = puz_file.readlines()
        for i in range(len(images)):
            images[i] = images[i].split()
            images[i][0] = int(images[i][0].strip(':'))

    # checks that puzzle number is valid        
    if number not in [4, 9, 16]:
        error_logger('Tile Number Error', selection)
        puzz_error = turtle.Turtle()
        puzz_error.shape('Resources/file_error.gif')
        time.sleep(4)
        puzz_error.ht()
        return False

    # checks that tile size is valid 
    elif not 50 <= size <= 110:
        error_logger('Tile Size Error', selection)
        puzz_error = turtle.Turtle()
        puzz_error.shape('Resources/file_error.gif')
        time.sleep(4)
        puzz_error.ht()
        return False

    # checks that all necessary tile images exist
    for i in range(len(images)):
        if not os.path.exists(images[i][1]):
            error_logger('Tile File Error', images[i][1])
            puzz_error = turtle.Turtle()
            puzz_error.shape('Resources/file_error.gif')
            time.sleep(4)
            puzz_error.ht()
            return False

    return True

def update_leaderboard(puzz):
    '''
    Function -- updates_leaderboard
        Updates the leaderboard in the Puzzle Slide game.
    Parameters:
        puzz (puzz) -- an instance of the puzz class
    Writes a new score to the Puzzle Slide game leaderboard. Creates a
    leaderboard file if none exists. Returns None.
    '''
    # check if leaderboard file exists
    try:
        with open('leaderboard.txt', mode='r') as leaderboard:
            # read the title line and the metadata line
            title = leaderboard.readline()
            metadata = leaderboard.readline()
            leaders = leaderboard.readlines()
            
        for i in range(len(leaders)):
            leaders[i] = leaders[i].split('\t')
            leaders[i][1] = int(leaders[i][1].strip('\n'))

        # add new score to the leaderboard and sort
        leaders.append([puzz.player_name, puzz.moves])
        leaders = sorted(leaders, key=lambda x: x[1])

        # remove highest score if more than 10 scores on leaderboard
        if len(leaders) > 10:
            leaders.pop()

        for i in range(len(leaders)):
            leaders[i][1] = str(leaders[i][1])
            leaders[i] = '\t'.join(leaders[i])
            leaders[i] = leaders[i] + '\n'

        # write new leaderboard to the leaderboard file
        with open('leaderboard.txt', mode='w') as leaderboard:
            leaderboard.write(title)
            leaderboard.write(metadata)
            for each in leaders:
                leaderboard.write(each)
                
    # if no leaderboard exists, create a new leaderboard file and write new
    # leaderboard to the file
    except FileNotFoundError:        
        with open('leaderboard.txt', mode='w') as leaderboard:
            leaderboard.write('LEADERBOARD\n')
            leaderboard.write('Name\tNumber of Moves\n')
            leaderboard.write(f'{puzz.player_name}\t{puzz.moves}\n')

def error_logger(error, file=None):
    '''
    Function -- error_logger
        Logs errors in the Puzzle Slider game.
    Parameters:
        error (str) -- name of the type of error
        file (str) -- optional parameter only used if a file error occurs.
                        Name of the file that caused the error
    Writes any encountered errors to and error file. Returns None.
    '''
    with open ('5001_puzzle.err', mode='a') as error_file:
        error_file.write(datetime.today().ctime())
        if error == 'Leaderboard Error':
                error_file.write(': Error: Could not open leaderboard.txt. ')
                error_file.write('LOCATION: game.create_gameboard()\n')
        elif error == 'Thumbnail Error':
            error_file.write(f': Error: Thumbnail file "{file}" does '\
                             'not exist. ')
            error_file.write('LOCATION: game.run_game_ui()\n')
        elif error == 'File Error':
            error_file.write(f': Error: Puzzle file "{file}" does '\
                             'not exist. ')
            error_file.write('LOCATION: game.load_func()\n')
        elif error == 'Tile Number Error':
            error_file.write(f': Error: Puzzle file "{file}" has '\
                             'invalid number of tiles. ')
            error_file.write('LOCATION: game.load_func()\n')
        elif error == 'Tile Size Error':
            error_file.write(f': Error: Puzzle tiles of "{file}" '\
                             'have invalid size. ')
            error_file.write('LOCATION: game.load_func()\n')
        elif error == 'Tile File Error':
            error_file.write(f': Error: Tile file "{file}" does '\
                             'not exist. ')
            error_file.write('LOCATION: game.load_func()\n')

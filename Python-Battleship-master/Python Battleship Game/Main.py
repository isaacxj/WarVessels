# Place.py

import random

import sys

#Import Documents
from Ships import Ships
from Coordinates import Coordinates
from Place import Place
from Shoot import Shoot
from ShotLocation import ShotLocation


#Welcome message with instructions
print("Welcome to WarVessels, a pass-and-play terminal game designed for OEC 2023! \n\
This game is based on the popular boardgame Battleship, but with some fun twists! \n\
You will be first asked to enter how big you want the grid size to be, between the sizes 5 x 5 to 10 x 10 \n\
You will be give 5 ships each taking 3 squares in a straight line \n\
Player 1 will place down 5 of their ships first, then player 2 \n\
To begin your turn you will roll a dice which decides whether your missiles misfire. \n\
If you roll a 1 or a 2 - you will get no missiles that turn. :( \n\
Then after you will each take turn shoot at certain location of the grid to try and hit your opponents ships \n\
Hitting an opponents ship grants you another turn and missing will skip your turn \n\
The aim of the game is to try and shoot down all of your opponents ships \n\
After choosing your grid size you will be asked to input commands, The command lists are as follows \n\n\
!!!During ship placements!!!\n\
place *orientation(h - horizontal/v - vertical),x_coordinate,y_coordinate* --- places a 3 long ship either vertically or horizontally at the given x y coordinates e.g    place h,0,0\n\
show ships --- shows your grid with ship placements 0 means empty and 1 is your ship location\n\
show coordinates --- shows the grid coordinates\n\
exit battleships --- exits the game\n\n\
Now After both players have placed placed their ships the shoot commands are as follows\n\n\
!!!During shooting phase!!!\n\
shoot x_coordinate,y_coordinate --- shoots at the request x y coordinates e.g   shoot 0,0\n\
show shots --- shows your shots in grid form where 0 means empty H means hit and X means miss\n\
show coordinates --- shows the grid coordinates\n\
exit warvessels\n\n\
Enjoy and have fun sinking each others ships\n")


def playerdiceRoll():
    print("Rolling the dice...")
    result = random.randint(1, 6)
    print(f"You got: {result}")
    if result >= 3:
        result_missile = 1
    else:
        result_missile = 0
    return result_missile

#Attributes
loop = True
loop_shoot = True
player_turn = 1
number_of_ships = 5

#Player1 and Player2 are Ships and can use the Ships and Place functions
player1 = Ships()
player2 = Ships()

#Player1 shoot grid and Player2 shoot grid are Shoot and can use the Shoot and ShotLocation functions
player1_shoot_grid = Shoot()
player2_shoot_grid = Shoot()

#coordinate map is of class Coordinates which prints the coordinate grid
coordinate_map = Coordinates()

#Asking the user to input grid size 
while loop:
    try:
        user_input = input("Please enter a number for the size of the grid between 8 and 10 ")
        user_input = user_input.lower()
        if user_input == "exit warvessels":
            sys.exit()
        grid_size = int(user_input)
        if grid_size >= 8 and grid_size <= 10:
            break
        
        else:
            print("Input must be between 8 and 10 \n")
    except ValueError:
        print("Please input a valid Integer \n")
        

#Creates a grid of 0's for the player ships to be placed on
grid_player1 = [["0"]*grid_size for n in range(grid_size)]
grid_player2 = [["0"]*grid_size for n in range(grid_size)]

#Creates a grid of 0's for the player hit or miss shots
shoot_grid_player1 = [["0"]*grid_size for n in range(grid_size)]
shoot_grid_player2 = [["0"]*grid_size for n in range(grid_size)]

#Creates a grid containing the coordinates "(0,1) (0,2 etc..."
grid_coordinates = [["0"]*grid_size for n in range(grid_size)]
i = 0
j = 0
while i < grid_size :
    while j < grid_size :
        grid_coordinates[i][j] = i,j
        j += 1
    j = 0
    i += 1

#Loop for player 1 placing ships
while loop:
    #User commands
    try:
        #Breaking the 2 inputs and assigning them as command and variable respectively
        command, variable = input("Player 1 please enter a command ").split()
        command = command.lower()
        variable = variable.lower()
        
        #If exit is inputed
        if command == "exit":
            if variable == "warvessels":
                sys.exit()
            else:
                print("Invalid exit command, Please input a valid exit command\n")

        #If show is inputed
        if command == "show":
            if variable == "ships":
                player1.show_ships(number_of_ships, grid_player1)
                
            if variable == "coordinates":
                coordinate_map.show_coordinates(grid_size, grid_coordinates)
                
            if variable != "ships" and variable != "coordinates":
                print("Invalid show command, Please input a valid show command\n")
            
        #If place is inputed
        if command == "place":
            try:
                #Breaking down the variable into 3 parts with , as the seperators and assigning them to orientation, x_coordinate_string and y_coordinate_string respectively
                orientation, x_coordinate_string, y_coordinate_string = variable.split(',')

                #Catching to see if x and y coordinates are ints 
                try:
                    x_coordinate = int(x_coordinate_string)
                    y_coordinate = int(y_coordinate_string)

                    #If statments check to see orientation and if x and y coordinates are valid in bound coordinates. Also checks to see if there is overlap in ship placements
                    if orientation == "v":
                        if x_coordinate >=0 and x_coordinate+2 < grid_size:
                            if y_coordinate >= 0 and y_coordinate <grid_size:
                                if grid_player1[x_coordinate][y_coordinate] != "1" and grid_player1[x_coordinate+1][y_coordinate] != "1" and grid_player1[x_coordinate+2][y_coordinate] != "1":

                                    #If eveything is okay will place a ship at the coordinates in the correct orientation
                                    player1.place_ship(orientation, x_coordinate, y_coordinate, grid_player1)
                                    number_of_ships = number_of_ships -1

                                    #If all ships are placed it will break the player 1 placement loop and player 2 placement loop will being.
                                    if number_of_ships == 0:
                                        break
                                    else:
                                        player1.show_ships(number_of_ships, grid_player1)
                                else:
                                    print("Please enter another coordinate, a ship has been place on one or more of the desired cooridinates\n")
                            else :
                                print("y coordinate out of bounds, Please enter a valid y coordinate\n")
                        else:
                            print("x coordinate out of bounds, Please enter a valid x coordinate\n")

                    #If statments check to see orientation and if x and y coordinates are valid in bound coordinates. Also checks to see if there is overlap in ship placements
                    if orientation == "h":
                        if x_coordinate >=0 and x_coordinate < grid_size:
                            if y_coordinate >= 0 and y_coordinate+2 <grid_size:
                                if grid_player1[x_coordinate][y_coordinate] != "1" and grid_player1[x_coordinate][y_coordinate+1] != "1" and grid_player1[x_coordinate+2][y_coordinate+2] != "1":

                                    #If eveything is okay will place a ship at the coordinates in the correct orientation
                                    player1.place_ship(orientation, x_coordinate,y_coordinate, grid_player1)
                                    number_of_ships = number_of_ships -1

                                    #If all ships are placed it will break the player 1 placement loop and player 2 placement loop will being.
                                    if number_of_ships == 0:
                                        break
                                    else:
                                        player1.show_ships(number_of_ships, grid_player1)
                                else:
                                    print("Please enter another coordinate, a ship has been place on one or more of the desired cooridinates\n")
                            else:
                                print("y coordinate out of bounds, Please enter a valid y coordinate\n")
                        else:
                            print("x coordinate out of bounds, Please enter a valid x coordinate\n")

                    #If orientation is not h and v then print invalid message
                    if orientation != "h" and orientation != "v":
                        print("Invalid orientation, Please enter a valid orientation either h or v, h for horizontal orientation and v for vertical orientation\n")

                except ValueError:
                    print("Please enter valid x and y coordinates\n")
                    
            except ValueError:
                print("Invalid place values, Please enter valid places values in the form orientation,x_coordinate,_y_coordinate\n")

        #If command is not exit, show and place then print invalid message        
        if command != "exit" and command != "show" and command != "place":
            print("Invalid command, Please input a valid command\n")

    except ValueError:
        print("Invalid command, Please input a valid command\n")


#Resets the number of ships back to 5 for player 2
number_of_ships = 5


#Clearing the game board so users cannot see each others boards
print("\n" * 100)
print("\n" * 100)
print("\n" * 100)
print("\n" * 100)
print("\n" * 100)

print("Player 1 has placed all their ships\n")


    
#Loop for player 2 placing ships
#!!!!Uses the same If statments and functions as the previous loop, but change the player grid to player 2
while loop:
    #User commands
    try:
        command, variable = input("Player 2 please enter a command ").split()

        #Lower cases both command and variable
        command = command.lower()
        variable = variable.lower()
        
        #If exit is inputed
        if command == "exit":
            if variable == "warvessels":
                sys.exit()
            else:
                print("Invalid exit command, Please input a valid exit command\n")

        #If show is inputed
        if command == "show":
            if variable == "ships":
                player2.show_ships(number_of_ships, grid_player2)
                
            if variable == "coordinates":
                player2.show_coordinates()
                
            if variable != "ships" and variable != "coordinates":
                print("Invalid show command, Please input a valid show command\n")
            
        #If place is inputed
        if command == "place":
            try:
                orientation, x_coordinate_string, y_coordinate_string = variable.split(',')

                #Catching to see if x and y coordinates are ints 
                try:
                    x_coordinate = int(x_coordinate_string)
                    y_coordinate = int(y_coordinate_string)
                
                    if orientation == "v":
                        if x_coordinate >=0 and x_coordinate+2 < grid_size:
                            if y_coordinate >= 0 and y_coordinate <grid_size:
                                if grid_player2[x_coordinate][y_coordinate] != "1" and grid_player2[x_coordinate+1][y_coordinate] != "1" and grid_player2[x_coordinate+2][y_coordinate] != "1":
                                    player2.place_ship(orientation, x_coordinate, y_coordinate, grid_player2)
                                    number_of_ships = number_of_ships -1
                                    
                                    if number_of_ships == 0:
                                        break
                                    else:
                                        player2.show_ships(number_of_ships, grid_player2)
                                else:
                                    print("Please enter another coordinate, a ship has been place on one or more of the desired cooridinates\n")
                            else :
                                print("y coordinate out of bounds, Please enter a valid y coordinate\n")
                        else:
                            print("x coordinate out of bounds, Please enter a valid x coordinate\n")

                    if orientation == "h":
                        if x_coordinate >=0 and x_coordinate < grid_size:
                            if y_coordinate >= 0 and y_coordinate+2 <grid_size:
                                if grid_player2[x_coordinate][y_coordinate] != "1" and grid_player2[x_coordinate][y_coordinate+1] != "1" and grid_player2[x_coordinate+2][y_coordinate+2] != "1":
                                    player2.place_ship(orientation, x_coordinate,y_coordinate, grid_player2)
                                    number_of_ships = number_of_ships -1
                                    if number_of_ships == 0:
                                        break
                                    else:
                                        player2.show_ships(number_of_ships, grid_player2)
                                else:
                                    print("Please enter another coordinate, a ship has been place on one or more of the desired cooridinates\n")
                            else:
                                print("y coordinate out of bounds, Please enter a valid y coordinate\n")
                        else:
                            print("x coordinate out of bounds, Please enter a valid x coordinate\n")

                    
                    if orientation != "h" and orientation != "v":
                        print("Invalid orientation, Please enter a valid orientation either h or v, h for horizontal orientation and v for vertical orientation\n")

                except ValueError:
                    print("Please enter valid x and y coordinates\n")

            except ValueError:
                print("Invalid place values, Please enter valid places values in the form orientation,x_coordinate,_y_coordinate\n")

        if command != "exit" and command != "show" and command != "place":
            print("Invalid command, Please input a valid command\n")

    except ValueError:
        print("Invalid command, Please input a valid command\n")


#Clearing the game board so users cannot see each others boards
print("\n" * 100)
print("\n" * 100)
print("\n" * 100)
print("\n" * 100)
print("\n" * 100)

print("Player 2 has placed all their ships\n")
print("Both Players have placed their ships. TIME FOR WAR!!! ")
print("Each player will now take turns to shoot down each others ships, if you hit a ship you get to shoot again")
print("The command to fire at the desired location is shoot(x coordinate, y coordinate) i.e shoot(5,8)\n")


#Loop where each player takes a turn to shoot down all of the opponents ships
while loop_shoot:
    
    #Checking to see if its player 1's turn
    dice = playerdiceRoll()
    if player_turn == 1 and dice == 1:
        
        try:
            #Splits the input and assigns it to shoot_command and shoot_coordinates respectively
            shoot_command, shoot_coordinates = input("Player 1 please enter your shoot command in the form (shoot x coordinate,y coordinate)\n\
please do not include the brackets but make sure you enter a comma to seperate the coordinates and a space to seperate the command and the coordinates.\n\
Replace x coordinate and y coordinate with the desired digits. You can also type (show shots) without any brackets to show where you have missed or hit\n\
Typing (show coordinates) without any brackets will display the coordinate grid ").split()
            print(" ")

            #Lower cases shoot_command
            shoot_command.lower()

            #If shoot is inputed
            if shoot_command == "shoot":

                    try:
                        #Splits the shoot_coordinates into shoot x and shoot y coordinates respectively
                        shoot_x_coordinate, shoot_y_coordinate = shoot_coordinates.split(',')

                        #Casts the input into an Integer
                        shoot_x_coordinate = int(shoot_x_coordinate)
                        shoot_y_coordinate = int(shoot_y_coordinate)

                        #Checking to see if the X and Y coordinates inputed is in bounds
                        if shoot_x_coordinate >= 0 and shoot_x_coordinate < grid_size and shoot_y_coordinate >=0 and shoot_y_coordinate < grid_size:

                            #Calls the method shoot_at_location and will return either 1 or 2 to see whos players turn it is depending if it was a hit or miss
                            player_turn = player2_shoot_grid.shoot_at_location(shoot_x_coordinate, shoot_y_coordinate, grid_player2, shoot_grid_player2, player_turn, player2_shoot_grid)

                            #Checks to see if all of the player's ships grid is 0, if True Display a winning message and break the loop. Game ends
                            if all(all(item == "0" for item in items) for items in grid_player2):
                                print("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\
                Game Over\n\n\
    Player 1 sunk all Player 2's ships\n\n\
                Player 1 Wins the war!\n\
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                loop_shoot = False

                        else:
                            print("Out of bounds, Please enter x and y coordinates between 0 and", grid_size -1)
                            print(" ")

                    except ValueError:
                        print("Please enter valid x and y coordinates\n")

            #If show is inputed
            if shoot_command == "show":
                try:
                    #Lower cases shoot_coordinates
                    shoot_coordinates.lower()

                    #If show shots is inputed then display the opponents shoot grid
                    if shoot_coordinates == "shots":
                        player2_shoot_grid.show_shots(shoot_grid_player2)

                    #If show coordinates is inputed print the coordinate grid    
                    if shoot_coordinates == "coordinates":
                        coordinate_map.show_coordinates(grid_size, grid_coordinates)

                    #If neither show shots or show coordinates is inputed then print invalid message       
                    if shoot_coordinates != "shots" and shoot_coordinates != "coordinates":
                        print("Please enter a valid show command\n")
                except ValueError:
                    print("Please enter a valid show command\n")

            #If exit is inputed
            if shoot_command == "exit":
                #Lower cases shoot_coordinates
                shoot_coordinates.lower()

                #If exit battleships is inputed then close/end game, else print invalid message
                if shoot_coordinates == "warvessels":
                    sys.exit()    
                else:
                    print("Enter a valid exit command")
                    
            #If neither shoot, show and exit is inputed then print invalid message        
            if shoot_command != "shoot" and shoot_command != "show" and shoot_command !="exit":
                print("Please enter a valid shoot command i.e shoot 0,0\n")


        except ValueError:
            print("Invalid command, Please input a valid command\n")
    if player_turn == 1 and dice == 0:
        print("Dice says your missiles jammed! Better Luck Next Time Player 1")
        player_turn = 2

    dice = playerdiceRoll()
    #Checking to see if its player 2's turn
    #Basically the same as the statments as player 1's shoot turn but change the grid_player and grid_shoot_player to player 1 and player turn = 2
    if player_turn == 2 and dice == 1:
        try:
            shoot_command, shoot_coordinates = input("Player 2 please enter your shoot command in the form (shoot x coordinate,y coordinate)\n\
please do not include the brackets but make sure you enter a comma to seperate the coordinates and a space to seperate the command and the coordinates. \n\
Replace x coordinate and y coordinate with the desired digits. You can also type (show shots) without any brackets to show where you have missed or hit\n\
Typing (show coordinates) without any brackets will display the coordinate grid ").split()
            print(" ")
            shoot_command.lower()
            if shoot_command == "shoot":
                try:
                    shoot_x_coordinate, shoot_y_coordinate = shoot_coordinates.split(',')
                    shoot_x_coordinate = int(shoot_x_coordinate)
                    shoot_y_coordinate = int(shoot_y_coordinate)
                    if shoot_x_coordinate >= 0 and shoot_x_coordinate < grid_size and shoot_y_coordinate >=0 and shoot_y_coordinate < grid_size:
                        player_turn = player1_shoot_grid.shoot_at_location(shoot_x_coordinate, shoot_y_coordinate, grid_player1, shoot_grid_player1, player_turn, player1_shoot_grid)
                        
                        if all(all(item == "0" for item in items) for items in grid_player1):
                            print("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\
            Game Over\n\n\
Player 2 sunk all Player 1's ships\n\n\
            Player 2 Wins the war!\n\
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            loop_shoot = False
                        
                    else:
                        print("Out of bounds, Please enter x and y coordinates between 0 and", grid_size -1)
                        print(" ")

                    
                except ValueError:
                    print("Please enter valid x and y coordinates\n")
                    
            if shoot_command == "show":
                try:
                    shoot_coordinates.lower()
                    if shoot_coordinates == "shots":
                        player1_shoot_grid.show_shots(shoot_grid_player1)
                        
                    if shoot_coordinates == "coordinates":
                        coordinate_map.show_coordinates(grid_size, grid_coordinates)
                        
                    if shoot_coordinates != "shots" and shoot_coordinates != "coordinates":
                        print("Please enter a valid show command\n")
                except ValueError:
                    print("Please enter a valid show command\n")

            if shoot_command == "exit":
                shoot_coordinates.lower()
                if shoot_coordinates == "warvessels":
                    sys.exit()
                else:
                    print("Enter a valid exit command")
                    
            if shoot_command != "shoot" and shoot_command != "show" and shoot_command !="exit":
                print("Please enter a valid shoot command i.e shoot 0,0\n")

        except ValueError:
            print("Invalid command, Please input a valid command\n")
    if player_turn == 2 and dice == 0:
        print("Dice says your missiles jammed! Better Luck Next Time Player 2")
        player_turn = 1



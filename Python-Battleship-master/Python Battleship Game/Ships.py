# Coordinates.py
#
# @ author: Anthony. Danial
# date: November 2018

#Prints the player grid with the ships in it
from Place import Place
class Ships(Place):
    
    def show_ships(self, number_of_ships, grid_player):
        print(" ")
        for row in grid_player:
            print (" ".join(row))
        print("\nThere are",number_of_ships, "ships left to place \n")

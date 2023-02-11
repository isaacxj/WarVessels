# Coordinates.py
#
# @ author: Anthony. Danial
# date: November 2018

#Prints the coordinate grid to the player
class Coordinates:
    def show_coordinates(self, grid_size, grid_coordinates):
        i = 0
        j = 0
        print(" ")
        while i < grid_size :
            while j < grid_size :
                print(grid_coordinates[i][j], end=" ")
                j += 1
            print("\n")
            j = 0
            i += 1
        print(" ")

# Coordinates.py
#
# @ author: Anthony. Danial
# date: November 2018

#Prints players hit or miss grid
class ShotLocation:
    def show_shots(self,shoot_grid):
        print(" ")
        for row in shoot_grid:
            print (" ".join(row))
        print(" ")


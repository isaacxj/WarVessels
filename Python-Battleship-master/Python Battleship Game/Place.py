# Place.py
#
# @ author: Anthony. Danial
# date: November 2018

#Depending on orientation, places the ship on designated players grid either 3 to the right or 3 down
class Place:
    def place_ship(self, orientation,x,y, grid_player):
        if orientation == "v":
            grid_player[x][y] = "1"
            grid_player[x+1][y] = "1"
            grid_player[x+2][y] = "1"

        if orientation == "h":
            grid_player[x][y] = "1"
            grid_player[x][y+1] = "1"
            grid_player[x][y+2] = "1"

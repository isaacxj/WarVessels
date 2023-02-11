# Coordinates.py
#
# @ author: Anthony. Danial
# date: November 2018

#Checking if shot location is a hit or miss
from ShotLocation import ShotLocation
class Shoot(ShotLocation):
    
    def shoot_at_location(self,x,y, grid_player, shoot_grid, player_turn, grid):
        if grid_player[x][y] == "1":
            if shoot_grid[x][y] == "0":
                print("Hit, Have another turn\n")
                shoot_grid[x][y] = "H"
                grid_player[x][y] = "0"
                grid.show_shots(shoot_grid)
                if player_turn == 1:
                    return(1)
                else:
                    return(2)
                
        else:
            if grid_player[x][y] == "0":
                if shoot_grid[x][y] == "0":
                    print("\n" * 100)
                    print("Miss, Next players turn\n")
                    shoot_grid[x][y] = "X"
                    if player_turn == 1:
                        return(2)
                    else:
                        return(1)
                else:
                    print("\n" * 100)
                    print("Miss, You have already shot there, next players turn\n")
                    if player_turn == 1:
                        return(2)
                    else:
                        player_turn = 1
                        return(1)

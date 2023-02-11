# Python-Battleship
2 player python battleship game

Make sure python of at least version 2.7 or higher is installed

The game is a text-based battleship game where you can play battle ships locally

Run the Main.py file to start the game

***Instructions***

You will be first asked to enter how big you want the grid size to be, between the sizes 5 x 5 to 10 x 10

You will be give 5 ships each taking 3 squares in a straight line

Player 1 will place down 5 of their ships first then player 2

Then after you will each take turn shoot at certain location of the grid to try and hit your opponents ships

Hitting an opponents ship grants you another turn and missing will skip your turn

The aim of the game is to try and shoot down all of your opponents ships

After choosing your grid size you will be asked to input commands, The command lists are as follows 

***!!!During ship placements!!!***

place *orientation(h - horizontal/v - vertical),x_coordinate,y_coordinate* --- places a 3 long ship either vertically or horizontally at the given x y coordinates e.g    place h,0,0

show ships --- shows your grid with ship placements 0 means empty and 1 is your ship location

show coordinates --- shows the grid coordinates

exit battleships --- exits the game

Now After both players have placed placed their ships the shoot commands are as follows

***!!!During shooting phase!!!***

shoot x_coordinate,y_coordinate --- shoots at the request x y coordinates e.g   shoot 0,0

show shots --- shows your shots in grid form where 0 means empty H means hit and X means miss

show coordinates --- shows the grid coordinates

exit battleships --- exits the game

Enjoy and have fun sinking each others ships

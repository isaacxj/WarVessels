from tkinter import Grid

import pygame
import random

# Define the screen dimensions and colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0, 0, 0)
GRID_COLOR = (255, 255, 255)
SHIP_COLOR = (0, 255, 0)
MISSILE_COLOR = (255, 0, 0)

# Define the grid dimensions and ship sizes
GRID_SIZE = 6
SHIP_SIZES = [2, 3, 3, 4]

# Define the game state variables
players = []
current_player_index = 0
game_over = False

# Initialize the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battleship")

# Define the functions for the game
def draw_grid(x, y, width, height, color):
    """
    Draw a grid on the screen.
    """
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, color, (x, y+i*height/GRID_SIZE), (x+width, y+i*height/GRID_SIZE))
        pygame.draw.line(screen, color, (x+i*width/GRID_SIZE, y), (x+i*width/GRID_SIZE, y+height))

def draw_ships(player):
    """
    Draw the ships on the screen.
    """
    for ship in player.ships:
        for (x, y) in ship.coords:
            pygame.draw.rect(screen, SHIP_COLOR, (x*SCREEN_WIDTH/GRID_SIZE, y*SCREEN_HEIGHT/GRID_SIZE, SCREEN_WIDTH/GRID_SIZE, SCREEN_HEIGHT/GRID_SIZE))

def draw_missiles(player):
    """
    Draw the missiles on the screen.
    """
    for (x, y) in player.missiles:
        pygame.draw.rect(screen, MISSILE_COLOR, (x*SCREEN_WIDTH/GRID_SIZE, y*SCREEN_HEIGHT/GRID_SIZE, SCREEN_WIDTH/GRID_SIZE, SCREEN_HEIGHT/GRID_SIZE))

def draw_screen():
    """
    Draw the game screen.
    """
    screen.fill(BG_COLOR)
    draw_grid(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_COLOR)
    draw_ships(players[current_player_index])
    draw_missiles(players[current_player_index])
    pygame.display.flip()

def check_ship_sunk(player, ship):
    """
    Check if a ship has been sunk.
    """
    for (x, y) in ship.coords:
        if (x, y) not in player.missiles:
            return False
    return True

def check_game_over():
    """
    Check if the game is over.
    """
    for player in players:
        for ship in player.ships:
            if not check_ship_sunk(player, ship):
                return False
    return True

class Ship:
    def __init__(self, size):
        self.size = size
        self.coords = []
        self.direction = None

    def place(self, x, y, direction):
        self.direction = direction
        if direction == "horizontal":
            for i in range(self.size):
                self.coords.append((x+i, y))
        else:
            for i in range(self.size):
                self.coords.append((x, y+i))

    def overlaps(self, other_ship):
        for (x, y) in self.coords:
            if (x, y) in other_ship.coords:
                return True
        return False

class Player:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.grid = Grid()
        self.offense_grid = Grid()
        self.shields = []
        self.missiles = 0

    def initialize_grid(self):
        print(f"{self.name}, please set up your ships on the 6x6 grid.")
        self.grid.print_grid()
        for i in range(4):
            length = i + 2
            print(f"Please set up your {length} square long ship.")
            while True:
                x, y = input("Enter the coordinates of the first square: ").split()
                direction = input("Enter the direction of the ship (up, down, left, or right): ")
                if self.grid.add_ship(int(x), int(y), direction, length):
                    break
                print("Invalid ship placement. Try again.")
            self.grid.print_grid()

    def initialize_shields(self):
        print(f"{self.name}, please roll a die to determine the number of shields you can place (1-6): ")
        roll = random.randint(1, 6)
        print(f"You rolled a {roll}")
        if roll < 3:
            print("Sorry, you get no shields this turn.")
        else:
            print(f"Place {roll} shields on your grid.")
            for i in range(roll):
                while True:
                    x, y = input(f"Enter the coordinates of shield #{i+1}: ").split()
                    if self.grid.add_shield(int(x), int(y)):
                        self.shields.append((int(x), int(y)))
                        break
                    print("Invalid shield placement. Try again.")
            self.grid.print_grid()

    def initialize_missiles(self):
        print(f"{self.name}, please roll a die to determine the number of missiles you can shoot (1-6): ")
        roll = random.randint(1, 6)
        print(f"You rolled a {roll}")
        if roll == 1:
            print("Sorry, you can't shoot any missiles this turn.")
        else:
            print(f"Shoot {roll} missiles on your opponent's grid.")
            self.missiles = roll

    def take_turn(self, opponent):
        print(f"{self.name}, it's your turn.")
        while True:
            pin = input("Enter your pin code to start your turn: ")
            if pin == self.pin:
                break
            print("Incorrect pin code. Try again.")
        self.initialize_shields()
        self.offense_grid.print_grid()
        if self.missiles > 0:
            for i in range(self.missiles):
                while True:
                    x, y = input(f"Enter the coordinates of missile #{i+1}: ").split()
                    if self.offense_grid.shoot(int(x), int(y)):
                        break
                    print("Invalid missile target. Try again.")
                self.offense_grid.print_grid()
        else:
            print("No missiles to shoot this turn.")
        self.missiles = 0
        opponent.grid.check_hits(self.offense_grid)
        self.offense_grid.reset()
        self.shields = []
class Game:
    def __init__(self):
        self.players = [Player(1), Player(2)]
        self.current_player = 0
        
    def start(self):
        self.setup_game()
        self.play_game()
        
    def setup_game(self):
        for player in self.players:
            self.setup_player(player)
    
    def setup_player(self, player):
        print(f"\nPlayer {player.number}, please setup your ships:")
        player_board = Board()
        for ship_size in [2, 3, 3, 4]:
            self.setup_ship(player_board, ship_size)
        player.board = player_board
    
    def setup_ship(self, board, ship_size):
        while True:
            print(f"Please select {ship_size} grid spaces for your ship (ex. A1, A2, A3):")
            ship_positions = input().upper().split()
            if len(ship_positions) != ship_size:
                print(f"Error: You must select {ship_size} grid spaces.")
                continue
            if not board.is_valid_positions(ship_positions):
                print("Error: Invalid positions selected.")
                continue
            if not board.is_free_positions(ship_positions):
                print("Error: Positions already occupied by another ship.")
                continue
            break
        board.add_ship(ship_positions)
class Game:
    def __init__(self):
        self.players = [Player(1), Player(2)]
        self.current_player = 0
        
    def start(self):
        self.setup_game()
        self.play_game()
        
    def setup_game(self):
        for player in self.players:
            self.setup_player(player)
    
    def setup_player(self, player):
        print(f"\nPlayer {player.number}, please setup your ships:")
        player_board = Board()
        for ship_size in [2, 3, 3, 4]:
            self.setup_ship(player_board, ship_size)
        player.board = player_board
        
    def setup_ship(self, board, ship_size):
        while True:
            print(f"Please select {ship_size} grid spaces for your ship (ex. A1, A2, A3):")
            ship_positions = input().upper().split()
            if len(ship_positions) != ship_size:
                print(f"Error: You must select {ship_size} grid spaces.")
                continue
            if not board.is_valid_positions(ship_positions):
                print("Error: Invalid positions selected.")
                continue
            if not board.is_free_positions(ship_positions):
                print("Error: Positions already occupied by another ship.")
                continue
            break
        board.add_ship(ship_positions)
    
    def play_game(self):
        print("\nAll ships placed. Let's begin the game!")
        while not self.is_game_over():
            self.switch_player()
            self.play_turn()
        self.end_game()
        
    def is_game_over(self):
        return all(ship.is_sunk() for player in self.players for ship in player.board.ships)
    
    def switch_player(self):
        self.current_player = (self.current_player + 1) % 2
        
    def play_turn(self):
        player = self.players[self.current_player]
        print(f"\nPlayer {player.number}, it's your turn.")
        pin = input("Please enter your pin: ")
        if pin != player.pin:
            print("Error: Incorrect pin.")
            return self.play_turn()
        print("Defense phase:")
        player.defend()
        print("Offense phase:")
        player.attack()
        
    def end_game(self):
        winner = self.get_winner()
        print(f"\nGame over! {winner.name} wins!")
        
    def get_winner(self):
        for player in self.players:
            if all(ship.is_sunk() for ship in player.board.ships):
                return player
        return None
def check_win(player, opponent):
    for ship in opponent.ships:
        if not ship.is_sunk():
            return False
    print(f"{player.name} wins!")
    return True
def play_game(player1, player2):
    game_over = False
    while not game_over:
        # Player 1 turn
        print(f"{player1.name}'s turn")
        player1_pin = input("Enter your PIN: ")
        while player1_pin != player1.pin:
            print("Incorrect PIN. Try again.")
            player1_pin = input("Enter your PIN: ")
        player1_defense_roll = roll_dice()
        player1_defense = player1.defend(player2.attack_grid, player1_defense_roll)
        print(f"{player1.name} defends grid space {player1_defense}")
        player1_offense_roll = roll_dice()
        player1_num_missiles = get_num_missiles(player1_offense_roll)
        player1_targets = get_targets(player2.ship_grid, player1_num_missiles)
        print(f"{player1.name} attacks {player1_targets}")
        player1.update_grids(player2, player1_targets)
        player1.display_grids()
        game_over = check_win(player1, player2)
        if game_over:
            break

        # Player 2 turn
        print(f"{player2.name}'s turn")
        player2_pin = input("Enter your PIN: ")
        while player2_pin != player2.pin:
            print("Incorrect PIN. Try again.")
            player2_pin = input("Enter your PIN: ")
        player2_defense_roll = roll_dice()
        player2_defense = player2.defend(player1.attack_grid, player2_defense_roll)
        print(f"{player2.name} defends grid space {player2_defense}")
        player2_offense_roll = roll_dice()
        player2_num_missiles = get_num_missiles(player2_offense_roll)
        player2_targets = get_targets(player1.ship_grid, player2_num_missiles)
        print(f"{player2.name} attacks {player2_targets}")
        player2.update_grids(player1, player2_targets)
        player2.display_grids()
        game_over = check_win(player2, player1)
        if game_over:
            break

    end_game(player1, player2)
def end_game(winner):
    # clear the screen
    screen.fill((255, 255, 255))

    # set the font and font size
    font = pygame.font.Font(None, 36)

    # create the text
    if winner == 1:
        text = font.render("Player 1 wins!", 1, (0, 0, 0))
    else:
        text = font.render("Player 2 wins!", 1, (0, 0, 0))

    # get the text rectangle
    text_rect = text.get_rect()

    # center the text
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery

    # blit the text
    screen.blit(text, text_rect)

    # update the display
    pygame.display.update()

    # wait for a short time before exiting
    pygame.time.delay(5000)
    pygame.quit()
    sys.exit()


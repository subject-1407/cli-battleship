#!/usr/bin/env python3
import random
from os import system, name

# # Constants
OCEAN_SIZE = 10
SHIPS = {'carrier': 5, 'battleship': 4, 'cruiser': 3, 'submarine': 3, 'destroyer': 2}
CHARS = ['#', '~', '@', 'o', 'x']


# # Ship setup functions

# Ships are elements of a dictionary with the names and sizes taken from SHIP_SIZES.
# The key is the ships name and the value is a list of tuples representing each part
# of the ship through an x- and y-coordinate and a bool for it is hit.
# E.g.: {'destroyer': [(0, 0, False), (0, 1, True)], ...}

# Check temp_ship against each ship in list of ships
# Returns True if a collision occurs
def check_for_collision(ships: dict, temp_ship: list):
    for ship in ships:
        for coordinates in ships[ship]:
            for temp_coordinates in temp_ship:
                if coordinates[0] == temp_coordinates[0] and coordinates[1] == temp_coordinates[1]:
                    return True
    return False


# Generate ship direction and random values for starting point x and y out of ship_size
# Calls check_for_collision to - well - check for a collision
# Calls itself if resulting ship would collide
# Returns ship
def place_ship_random(ships: dict, ship_size: int):
    vertical = random.randint(0, 1) == 0
    temp_ship = []
    if vertical:
        x = random.randint(0, OCEAN_SIZE - 1)
        y = random.randint(0, OCEAN_SIZE - 1 - ship_size - 1)
        for i in range(ship_size):
            temp_ship.append((x, y + i, False))
    else:
        x = random.randint(0, OCEAN_SIZE - 1 - ship_size - 1)
        y = random.randint(0, OCEAN_SIZE - 1)
        for i in range(ship_size):
            temp_ship.append((x + i, y, False))
    if check_for_collision(ships, temp_ship):
        return place_ship_random(ships, ship_size)
    else:
        return temp_ship


# Place ships random
# Calls place_ship_random for each ship
# Returns list of ships
def place_ships_random(ships: dict):
    for ship in SHIPS:
        ships.update({ship: place_ship_random(ships, SHIPS[ship])})
    return ships


# TODO Implement
def place_ships_manual(ships: dict):
    return ships


# # View updating functions

# A view is either the ocean or radar which you may or may not know from the actual battleship game.
# It is represented through a matrix of numbers, a number represents the state of the cell.
# 0: Fog
# 1: Water
# 2: Hit Water
# 3: Ship
# 4: Hit Ship

# Initializing view by filling a OCEAN_SIZE x OCEAN_SIZE Matrix with the given code
# Returns initialized view
def init_view(view: list, state: int):
    for i in range(OCEAN_SIZE):
        view.append([])
        for j in range(OCEAN_SIZE):
            view[i].append(state)
    return view


# Places dict of ships in view
# Returns view
def place_ships_in_view(view: list, ships: dict):
    for ship in ships:
        for coordinates in ships[ship]:
            x, y, hit = coordinates
            view[y][x] = 3
    return view


# Updates View taking a tuple and updating the hit cell
# Returns the updated view
def update_view(view: list, cell: tuple):
    x, y, hit = cell
    if not hit:
        view[y][x] = 2
    else:
        view[y][x] = 4
    return view


# # Interaction functions

# Output gets regularly cleared out and redrawn... you get why!
# For easier interaction the x-coordinates are translated to letters.
# The output uses the chars of CHARS rather than numbers.

# Clears the terminal
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


# Prints view on output using the chars from CHARS
def draw(view: list, prompt: str):
    clear()
    result = '#   '
    for i in range(len(view)):
        result += chr(ord('A') + i) + '   '
    for i in range(len(view)):
        result += '\n\n' + str(i) + '   '
        for j in range(len(view)):
            result += CHARS[view[i][j]] + '   '
    print(f'{result}\n\n')
    if prompt:
        input(prompt)


# # Marine navigation translator

# Marine coordinates use A, B, C, ... for x and 0, 1, 2, ... for y

# TODO Code
def code(mar_nav: str):
    return mar_nav


# TODO Document
def decode(x, y):
    return f'{chr(ord("A") + x)}{y}'


# # Game functions

# TODO Document
def shoot(ships: dict, x: int, y: int):
    for ship in ships:
        for i in range(len(ships[ship])):
            if x == ships[ship][i][0] and y == ships[ship][i][1]:
                ships[ship][i] = (x, y, True)
                return ships, (x, y, True)
    return ships, (x, y, False)


# TODO Document
def check_if_sunk(ships: dict):
    for ship in ships:
        result = True
        for coordinate in ships[ship]:
            if not coordinate[2]:
                result = False
                break
        if result:
            del ships[ship]
            return True


# TODO Document
def check_for_damage(ships: dict, impact_point: tuple):
    if not impact_point[2]:
        return 'Miss!'
    else:
        if not check_if_sunk(ships):
            return 'Hit!'
        else:
            return 'Hit sunk!'


# # AI

# TODO Document
def ai_aim(mode: str, memory: list):
    if mode == 'easy':
        x, y = random.randint(0, OCEAN_SIZE - 1), random.randint(0, OCEAN_SIZE - 1)
        if (x, y) in memory:
            x, y, memory = ai_aim(mode, memory)
        memory.append((x, y))
        return x, y, memory
    if mode == 'hard':
        # TODO Write actual AI
        pass

if __name__ == '__main__':

    # Initializing
    difficulty = ''
    enemy_ships = {}
    player_ships = {}
    radar = init_view([], 0)
    ocean = init_view([], 1)
    ai_memory = []

    # Difficulty selection
    difficulty_selected = False
    while not difficulty_selected:
        clear()
        difficulty = input('Select difficulty [easy/hard]: ')
        if difficulty == 'easy' or difficulty == 'hard':
            difficulty_selected = True
            enemy_ships = place_ships_random(enemy_ships)
        else:
            clear()
            input(f'"{difficulty}" is not an option!')

    # Ship setup
    placement_mode_selected = False
    while not placement_mode_selected:
        draw(ocean, '')
        placement_mode = input('Select how ships are to be placed [random/manual]: ')
        if placement_mode == 'random':
            placement_mode_selected = True
            player_ships = place_ships_random(player_ships)
        elif placement_mode == 'manual':
            placement_mode_selected = True
            player_ships = place_ships_manual(player_ships)
        else:
            draw(ocean, f'"{placement_mode}" is not an option!')
    ocean = place_ships_in_view(ocean, player_ships)
    draw(ocean, 'All ships are in position!')

    # Game Loop
    # if random.randint(0, 1) == 0:
    #     # AI Turn
    #     aim_x, aim_y, ai_memory = ai_aim(difficulty, ai_memory)
    #     player_ships, hit_or_miss = shoot(player_ships, x, y)
    #     ocean = update_view(ocean, hit_or_miss)
    #     draw(ocean)
    #     print(check_result(player_ships, hit_or_miss))
    while player_ships and enemy_ships:
        # TODO Player Turn
        # x, y = player_choose_spot(radar)
        # enemy_ships, hit_or_miss = shoot(enemy_ships, x, y)
        # radar = update_view(radar, hit_or_miss)
        # draw(radar)
        # print(check_result(enemy_ships, hit_or_miss))

        # AI Turn
        aim_x, aim_y, ai_memory = ai_aim(difficulty, ai_memory)
        draw(ocean, f'Opponent aims at {decode(aim_x, aim_y)}...')
        player_ships, struck_point = shoot(player_ships, aim_x, aim_y)
        ocean = update_view(ocean, struck_point)
        draw(ocean, check_for_damage(player_ships, struck_point))

    # End screen
    if player_ships:
        draw(radar, 'YOU WIN!')
    else:
        draw(ocean, 'YOU LOSE!')

    exit()

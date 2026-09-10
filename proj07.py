################################################################################
#
# Computer Project 07
# Description:
# This program allows users to run the game of Treasure Hunt in multiple
# rounds through a series of commands. Players can find treasures, fall
# in traps, or quit the game if desired. This program prominently uses
# classes to navigate the game, along with functions, classes, and more.
#
# The user is prompted to enter an integer between 2 and 4 for the number
# of players, and an integer between 5 and 8 for the size of the map. The
# number of treasures and traps is based on the map size. The game continues
# based on user input, and the game ends if all players quit, if any player
# reaches a score of at least 100, or if there are no treasures left.
################################################################################


# Allowed import statements
from treasure_hunt import Player, Map, Item

#------banner and rules (read-only)-----------------
banner = ("WELCOME TO THE TREASURE HUNT!\n"
"Ahoy, brave adventurers!\n"
"Prepare yourself for an epic journey across \nMAP OF LEGENDS where treasures glitter and \ntraps await the unwary!"
)

rules = (
"\nIn this game:\n- T represents Treasure (25 points)\n- X represents Trap (-5 points)\n- P represents Player"
"\n- . represents Empty space\nCollect treasures and avoid traps to win!\n"
)

direction_lst = ['up', 'down', 'left', 'right']
def display_menu():
    '''
    Display the banner and rules of the game
    Returns:
        None
    '''
    print(banner)
    print(rules)

def player_input():
    '''
    Prompts users for a number of players repeatedly until they
    enter a valid input.
    Valid inputs are integers between 2 and 4.
    Returns:
        Error message if input is invalid
        Number of players as an integer if input is valid
    '''

    global players
    while True:
        players = input(":~Enter the number of players (2-4) ~:")
        if players.isdigit() == False:
            print("Please enter a valid number")
        elif int(players) < 2 or int(players) > 4:
            print("Please enter a number between {} and {}".format(2, 4))
        else:
            break
    return int(players)

def map_input():
    '''
    Prompts users for a map size repeatedly until they enter
    a valid input.
    Valid inputs are integers between 5 and 8.
    Returns:
        Error message if input is invalid
        Size of map as an integer if input is valid
    '''

    global map_size
    while True:
        map_size = input("\n:~Enter the map size (5-8) ~:")
        if map_size.isdigit() == False:
            print("Please enter a valid number")
        elif int(map_size) < 5 or int(map_size) > 8:
            print("Please enter a number between {} and {}".format(5, 8))
        else:
            break
    return int(map_size)

def initialize_game(players, map_size):
    '''
    Initializes the game map.
    Initializes the number of treasures as the same size as of the map.
    Initializes traps as two less than the size of the map.
    Places the treasures and traps at randomly generated unique positions
    on the game map.
    Initialize player objects and place players on game map.
    Used positions are logged in order to ensure uniqueness.
    Args:
        players: number of players
        map_size: size of the map; dictates number of treasures and traps

    Returns:
        Updated game map
    '''

    global num_treasures
    num_treasures = map_size

    global num_traps
    num_traps = map_size - 2

    global game_map
    game_map = Map(size=map_size)

    used_pos = set()

    global treasures_lst
    treasures_lst = []

    global traps_lst
    traps_lst = []

    for i in range(num_treasures):
        while True:
            position = game_map.generate_random_position()
            if position not in used_pos:
                game_map.place_item(Item("Treasure"), position)
                used_pos.add(position)
                treasures_lst.append(position)
                break

    for i in range(num_traps):
        while True:
            position = game_map.generate_random_position()
            if position not in used_pos:
                game_map.place_item(Item("Trap"), position)
                used_pos.add(position)
                traps_lst.append(position)
                break

    global players_lst
    players_lst = []
    global players_pos
    players_pos = set()
    for i in range(1, players + 1):
        player_name = "Player#{}".format(i)
        while True:
            position = game_map.generate_random_position()
            if position not in used_pos:
                p = Player(name=player_name, position=position)
                game_map.add_player(p)
                players_lst.append(p)
                used_pos.add(position)
                players_pos.add(p.position)
                break
    return game_map

def display_start(players, map_size):
    '''
    Displays the start of the game.
    Includes formatted number of players and map size.
    Args:
        players: number of players
        map_size: size of the map

    Returns:
        None
    '''
    print("\n==================================================")
    print("Starting game with {} players on a {}x{} map".format(players, map_size, map_size))
    print("==================================================\n")

def players_status():
    '''
    Displays the status of the players.
    Uses .check_status from Player class in treasure_hunt.py
    Returns:
        None
    '''
    print("\nPlayers:")
    for p in players_lst:
        print(p.check_status())

def display_game_map(game_map):
    '''
    Displays the game map with treasures, traps, and players included.
    Args:
        game_map: updated game map

    Returns:
        None
    '''
    print("\nGame Map:{}".format(game_map.display()))
    print("\nTreasures remaining: {}".format(num_treasures))

def display_player_turn(player_name, position):
    '''
    Displays player turn.
    Gives directions for moving on the map.
    Args:
        player_name: current player's name
        position: current player's position

    Returns:
        Direction of player turn
    '''
    # display which players turn and directions on moving
    print("\n--------------------------------------------------")
    print("{}'s turn. Current position: {}".format(player_name, position))
    global direction
    direction = input(":~Enter direction (up/down/left/right) or 'quit' to leave ~:")
    print("--------------------------------------------------\n")
    return direction

#def player_direction(p):
    # moves a player in the correct direction, error message and skips
    global players_pos

    current_position = p.position
    valid = True

    if direction not in direction_lst:
        print("Invalid direction! Please try again.")
        return False

    new_position = p.move(direction)

    if not game_map.is_valid_move(new_position):
        print(f"Invalid move! {p.name} stays at {p.position}")
        return False

    for other in players_lst:
        if other != p and other.position == new_position:
            print(f"Position occupied by {other.name}! {p.name} stays at {p.position}")
            return False
    players_pos.remove(current_position)
    players_pos.add(new_position)
    p.position = new_position

    return True

#def player_move(p):
    # if move is invalid
    #if p.position in used_pos:

    # if valid, call update_position in main after player_move
    pass

#def update_position():
    # update position of player
    pass

def update_inventory(p):
    '''
    Collects item player landed on.
    Updates the inventory of a player.
    Args:
        p: player object

    Returns:
        None
    '''
    global num_treasures, num_traps
    if p.position in treasures_lst:
        item = game_map.remove_item(p.position)
        p.collect_item(item)
        print(f"{p.name} found Treasure! Score: {p.score}")
        num_treasures -= 1
        treasures_lst.remove(p.position)

    elif p.position in traps_lst:
        item = game_map.remove_item(p.position)
        p.collect_item(item)
        print(f"{p.name} fell into the Trap! Score: {p.score}")
        num_traps -= 1
        traps_lst.remove(p.position)
    else:
        print(f"{p.name} moved to {p.position}")


def remove_player(p):
    '''
    Removes a player from the game map.
    Ends their game and displays results.
    Args:
        p: player object

    Returns:
        None
    '''
    print(f"{p.name} has left the game!")
    if p.position in players_pos:
        players_pos.remove(p.position)
    game_map.remove_player(p.name)
    players_lst.remove(p)

def end_game():
    '''
    Ends the game.
    Displays message dependent on terms at end of game.
    Returns:
        True or False
    '''
    if len(players_lst) == 0:
        print("\n==================================================")
        print("Game Over! All players have quit!")
        print("==================================================")
        print("\nThanks for playing Treasure Hunt! Goodbye!")
        return True

    for p in players_lst:
        if p.score >= 100:
            print("\n==================================================")
            print(f"Game Over! {p.name} wins with score {p.score}!")
            print("==================================================")
            print("\nThanks for playing Treasure Hunt! Goodbye!")
            return True

    if len(treasures_lst) == 0:
        max_score = max(p.score for p in players_lst)
        top_players = [p for p in players_lst if p.score == max_score]

        if len(top_players) == 1:
            winner = top_players[0]
        else:
            min_traps = min(len([i for i in p.inventory if i.name == "Trap"]) for p in top_players)
            trap_filtered = [p for p in top_players if len([i for i in p.inventory if i.name =="Trap"]) == min_traps]
            if len(trap_filtered) == 1:
                winner = trap_filtered[0]
            else:
                winner = sorted(trap_filtered, key=lambda x: x.name)[0]
        print("\n==================================================")
        print(f"Game Over! {winner.name} wins with score {winner.score}!")
        print("==================================================")
        print("\nThanks for playing Treasure Hunt! Goodbye!")
    return False

def main():
    display_menu()
    player_input()
    map_input()

    display_start(players, map_size)
    game_map = initialize_game(int(players), int(map_size))

    players_status()
    display_game_map(game_map)
    while True:
        if not players_lst:
            print("\n==================================================")
            print("Game Over! All players have quit!")
            print("==================================================")
            print("\nThanks for playing Treasure Hunt! Goodbye!")
            break

        for p in players_lst[:]:
            while True:
                direction = display_player_turn(p.name, p.position)

                if direction == "quit":
                    remove_player(p)
                    if players_lst:
                        players_status()
                        display_game_map(game_map)
                    break

                if direction not in direction_lst:
                    print("Invalid direction! Please try again.")
                    continue

                new_position = p.move(direction)

                if not game_map.is_valid_move(new_position):
                    print(f"Invalid move! {p.name} stays at {p.position}")
                    players_status()
                    display_game_map(game_map)
                    break

                occupied = False
                for other in players_lst:
                    if other != p and other.position == new_position:
                        print(f"Position occupied by {other.name}! {p.name} stays at {p.position}")
                        occupied = True
                        break

                if occupied:
                    players_status()
                    display_game_map(game_map)
                    break

                players_pos.remove(p.position)
                players_pos.add(new_position)
                p.position = new_position
                update_inventory(p)

                players_status()
                display_game_map(game_map)
                break

            if end_game():
                return



if __name__ == "__main__":
    main()
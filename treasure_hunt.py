import random
random.seed(100)

class Item:
    """
    Represents an item in the game (Treasure or Trap).
    
    Attributes:
        name (str): Name of the item ('Treasure' or 'Trap')
        value (int): Point value of the item (25 for Treasure, -5 for Trap)
    """
    def __init__(self, name='Treasure'):
        """
        Initialize an Item.

        Args:
            name (str, optional): Name of the item. Defaults to 'Treasure'.
        """
        self.name = name
        self.value = 25 if name == 'Treasure' else -5

    def __str__(self):
        """Return string representation of the item."""
        return f"{self.name} (Value: {self.value})"

class Player:
    """
    Represents a player in the game.
    
    Attributes:
        name (str): Player's name
        position (tuple): Current position on the map as (x, y)
        inventory (list): List of collected items
        score (int): Current score based on collected items
    """
    def __init__(self, name, position):
        """
        Initialize a Player.

        Args:
            name (str): Player's name
            position (tuple): Starting position as (x, y)
        """
        self.name = name
        self.position = position
        self.inventory = []  # List of Item objects
        self.score = 0

    def move(self, direction):
        """
        Calculate new position based on movement direction.

        Args:
            direction (str): Direction to move ('up', 'down', 'left', 'right')

        Returns:
            tuple: New position as (x, y)
        """
        x, y = self.position
        if direction == "up":
            return x - 1, y
        elif direction == "down":
            return x + 1, y
        elif direction == "left":
            return x, y - 1
        elif direction == "right":
            return x, y + 1
        return self.position

    def collect_item(self, item: Item):
        """
        Add an item to player's inventory and update score.

        Args:
            item (Item): Item to collect
        """
        if item:
            self.inventory.append(item)
            self.score += item.value

    def check_status(self):
        """
        Get a string representation of player's current status.

        Returns:
            str: Formatted string with player's position, inventory, and score
        """
        if not self.inventory:
            inventory_str = "empty"
        else:
            treasure_count = sum(1 for item in self.inventory if item.name == 'Treasure')
            trap_count = sum(1 for item in self.inventory if item.name == 'Trap')
            inventory_parts = []
            if treasure_count > 0:
                if treasure_count == 1:
                    inventory_parts.append(f"{treasure_count} Treasure")
                else:
                    inventory_parts.append(f"{treasure_count} Treasures")
            if trap_count > 0:
                if trap_count == 1:
                    inventory_parts.append(f"{trap_count} Trap")
                else:
                    inventory_parts.append(f"{trap_count} Traps")
            inventory_str = ", ".join(inventory_parts)
        
        return f"    {self.name}:\n      Position: {self.position}\n      Inventory: {inventory_str}\n      Score: {self.score}"

class Map:
    """
    Represents the game map and manages game state.
    
    Attributes:
        size (int): Size of the square map (size x size)
        grid (list): 2D list representing the map grid
        players (dict): Dictionary of players on the map
        items (list): List of all items on the map
    """
    def __init__(self, size):
        """
        Initialize the Map.

        Args:
            size (int): Size of the square map (size x size)
        """
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.players = {}  # Dictionary of players on the map
        self.items = []  # List of all items on the map

    def add_player(self, player):
        """
        Add a player to the map.

        Args:
            player (Player): Player to add

        Returns:
            bool: True if player was successfully added, False otherwise
        """
        if player.name not in self.players and self.is_valid_move(player.position):
            self.players[player.name] = player
            return True
        return False

    def remove_player(self, player_name):
        """
        Remove a player from the map.

        Args:
            player_name (str): Name of player to remove

        Returns:
            Player or None: Removed player if found, None otherwise
        """
        return self.players.pop(player_name, None)

    def place_item(self, item, position):
        """
        Place an item on the map.

        Args:
            item (Item): Item to place
            position (tuple): Position to place item at as (x, y)

        Returns:
            bool: True if item was successfully placed, False otherwise
        """
        x, y = position
        if self.is_valid_move(position) and self.grid[x][y] is None:
            self.grid[x][y] = item
            self.items.append(item)


    def remove_item(self, position):
        """
        Remove and return an item from the map.

        Args:
            position (tuple): Position to remove item from as (x, y)

        Returns:
            Item or None: Removed item if found, None otherwise
        """
        x, y = position
        if self.is_valid_move(position) and self.grid[x][y] is not None:
            item = self.grid[x][y]
            self.grid[x][y] = None
            if item in self.items:
                self.items.remove(item)
            return item
        return None

    def get_item(self, position):
        """
        Get item at a position without removing it.

        Args:
            position (tuple): Position to check as (x, y)

        Returns:
            Item or None: Item at position if found, None otherwise
        """
        x, y = position
        if self.is_valid_move(position):
            return self.grid[x][y]
        return None

    def is_valid_move(self, position):
        """
        Check if a position is within map boundaries.

        Args:
            position (tuple): Position to check as (x, y)

        Returns:
            bool: True if position is valid, False otherwise
        """
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    def get_player_positions(self):
        """
        Get a dictionary of player positions.

        Returns:
            dict: Dictionary mapping positions to player names
        """
        return {player.position: player.name for player in self.players.values()}

    def generate_random_position(self):
        """
           Generate a random position within the game grid.

           Returns
           -------
           tuple of int
               A tuple (x, y) representing a random coordinate on the grid,
               where both x and y are integers between 0 and self.size - 1.
        """
        pos = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        return pos


    def display(self):
        """
        Get a string representation of the map.

        Returns:
            str: Map display with:
                - 'P' for players
                - 'T' for treasures
                - 'X' for traps
                - '.' for empty spaces
        """
        result = [""]
        player_positions = self.get_player_positions()
        
        for i in range(self.size):
            row_str = []
            for j in range(self.size):
                pos = (i, j)
                if pos in player_positions:
                    row_str.append("P")  # Player
                elif self.grid[i][j] is None:
                    row_str.append(".")  # Empty
                elif self.grid[i][j].value > 0:
                    row_str.append("T")  # Treasure
                else:
                    row_str.append("X")  # Trap
            result.append(" ".join(row_str))
        return "\n    ".join(result)

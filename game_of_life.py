import os
from random import randint

# get the number of character rows, columns of the screen 
# and convert into integers
rows, columns = os.popen('stty size', 'r').read().split()
num_rows = int(rows) - 1  # leave space for input
num_columns = int(columns)

# just because I hate polluting the global scope...
# we're going to use as many functions without side effects as possible

def get_empty_grid(c, r):
    """Initiate an empty grid."""
    grid = [[0 for x in range(c)] for y in range(r)]
    return grid


def copy_grid(grid):
    """Return a deep copy of the grid."""
    # Make a copy of each row and pass it in to a new row
    new_grid = [grid[y].copy() for y in range(len(grid))]
    return new_grid


def populate_grid(grid, num):
    """Given a grid, return a deep copy of the grid with randomly generated cells."""
    new_grid = copy_grid(grid)
    for i in range(num):
        y = randint(0, len(new_grid) - 1)
        x = randint(0, len(new_grid[y]) - 1)
        new_grid[y][x] = 1
    return new_grid


def print_grid(grid, icon):
    """Print the given grid to the console"""
    printed_grid = ""
    for row in grid:
        for cell in row:
            # the cell should be represented by the comment, if passed, otherwise by the number
            cell_icon = icon if icon else str(int(cell))
            # we only print when cell is occupied
            printed_grid += cell_icon if cell else " "
        printed_grid += "\n"
    # print to screen for fancy animation. (lol)
    print(printed_grid)


def get_num_neighbors(grid, x, y):
    """Given a grid and the cell coordinates, get the total number of neighbors"""
    # neighbor coordinates
    u = y - 1
    d = y + 1
    l = x - 1
    r = x + 1

    # neighbor coordinates valid
    u_valid = u >= 0
    d_valid = d < len(grid)
    l_valid = l >- 0

    r_valid = r < len(grid[y])
    
    # populations 
    pop = 0
    pop += 0 if not u_valid else grid[u][x] # pop_u
    pop += 0 if not d_valid else grid[d][x] # pop_d
    pop += 0 if not l_valid else grid[y][l] # pop_l
    pop += 0 if not r_valid else grid[y][r] # pop_r

    # diagonal populations
    pop += 0 if not (u_valid and l_valid) else grid[u][l] # pop_u_l
    pop += 0 if not (u_valid and r_valid)else grid[u][r] # pop_u_r
    pop += 0 if not (d_valid and l_valid)else grid[d][l] # pop_d_l
    pop += 0 if not (d_valid and r_valid)else grid[d][r] # pop_d_r

    return pop


def cell_survives(grid, x, y):
    """Given a grid and the cell coordinates, determine if the cell survives
        return 0 for no
        return 1 for yes"""
    num_neighbors = get_num_neighbors(grid, x, y)
    cell_alive = grid[y][x]
    if cell_alive:
      # rules of the game of life
      # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
      # Any live cell with two or three live neighbours lives on to the next generation.
      # Any live cell with more than three live neighbours dies, as if by overpopulation.
      return (num_neighbors == 2 or num_neighbors == 3)
    else:
      # rules of the game of life pt 2
      # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
      return (num_neighbors == 3)


def next_grid_state(grid):
    """Return the next grid state from the given grid state"""
    next_grid = copy_grid(grid)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            next_grid[y][x] = cell_survives(grid, x, y)
    return next_grid


def get_num_neighbors_grid(grid):
    """Return a grid with the number of neighbors per block"""
    num_grid = copy_grid(grid)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            num_grid[y][x] = get_num_neighbors(grid, x, y)
    return num_grid


# user defines the start of the game
user_input = input(
    'How many starting cells (default random # between 0 and 1000)? ')
default_num_cells = randint(1, 1000)
try:
    num_cells = int(user_input) if int(user_input) > 0 else default_num_cells
except:
    num_cells = default_num_cells
    
user_input = input('How many generations (default 800)? ')
default_maxcount = 800
try:
    maxcount = int(user_input) if int(user_input) > 0 else default_maxcount
except:
    maxcount = default_maxcount


# init the grid and populate it with cells
grid = get_empty_grid(num_columns, num_rows)
grid = populate_grid(grid, num_cells)

counter = 0
while counter < maxcount:
    # second parameter is the "icon" used to represent a living cell
    print_grid(grid, ".")
    grid = next_grid_state(grid)
    counter += 1
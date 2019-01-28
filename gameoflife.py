# Game of life technical test submission - written using Python 2.7
# James Wheeldon

import numpy as np
import pandas as pd

def create_grid(gridsize,seed):
    if seed == 'blank':
        grid = pd.DataFrame(np.random.randint(1,size=(gridsize,gridsize)))

    elif seed == 'oscillator':
        grid = pd.DataFrame(np.random.randint(1,size=(gridsize,gridsize)))
        grid.iloc[2,1:4] = [1,1,1]

    elif seed == 'random':
        np.random.seed(10)
        grid = pd.DataFrame(np.random.randint(2,size=(gridsize,gridsize)))

    elif seed == 'glider':
        grid = pd.DataFrame(np.random.randint(1,size=(gridsize,gridsize)))
        grid.iloc[1,1:4] = [1,0,0]
        grid.iloc[2,1:4] = [0,1,1]
        grid.iloc[3,1:4] = [1,1,0]

    else:
        pass

    print('=================================')
    print(grid)
    print('=================================')
    return grid

def create_life(freq):
    # Convert data-types and count frequency of neighbour overlaps
    tup = [tuple(coord) for coord in freq]
    flat = pd.Series(tup)
    counts = flat.value_counts()
    new = counts.index[counts == 3]
    return new

def evolve(grid):
    # Get grid shape from create_grid()
    grid_max_x, grid_max_y = grid.shape

    # Find each live cell co-ordinates and count neighbours
    coord = []
    neighbours_freq = []
    for x,y in zip(*np.where(grid.values == 1)):

        ## Define neighbours per live cell
        neighbours =    [(x-1,y-1), (x-1,y),    (x-1,y+1),
                        (x,y-1),                (x,y+1),
                        (x+1,y-1),  (x+1,y),    (x+1,y+1)]

        ## Count live neighbour interactions per live cell
        live_count = 0
        for i,j in neighbours:
            if 0 <= i < grid_max_x and 0 <= j < grid_max_y:
                live_count += grid.iloc[i,j]
                neighbours_freq.append([i,j])

        ## Append co-ordinates to list
        coord.append([x,y,live_count])

    # Rules of life
    for row, col, count in coord:
        grid.iloc[row,col] = count

        ## Scenario 0: No interactions
        if count == 0:
            grid.iloc[row,col] = 0

        ## Scenario 1: Underpopulation
        if count < 2:
            grid.iloc[row,col] = 0

        ## Scenario 2: Overcrowding
        if count > 3:
            grid.iloc[row,col] = 0

        ## Scenario 3: Survival
        if count == 2 or count == 3:
            grid.iloc[row,col] = 1

    # Scenario 4: Creation of new life
    live_new = create_life(neighbours_freq)
    for new_coord in live_new:
        grid.iloc[new_coord] = 1

    print(grid)
    print('=================================')

def main(gridsize, steps, seed):
    seed_valid = ['blank','oscillator','random','glider']

    if gridsize < 5:
        print('Error: Grid size is too small (min 5).')

    elif seed not in seed_valid:
        print('Error: Invalid seed type. Choose either blank, oscillator, random or glider.')

    else:
        grid = create_grid(gridsize, seed)
        for _ in range(steps):
            raw_input('Press any key to evolve:')
            evolve(grid)
            

# Game of life (Grid size, number of evolutions, seed type)
# Scenario 5: Grid with no live cells
#main(5,2,'blank')

# Scenario 6: Expected game outcome for seeded grid
main(5,2,'oscillator')

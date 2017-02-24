from collections import Counter

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows,cols)
row_units = [cross(r, cols) for r in rows]

column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[(rows[i]+cols[i]) for i in range(0, len(rows))], [(rows[8-i] + cols[i]) for i in range(0, len(rows))]]
unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): sudoku in dictionary form
    Returns:
        values(dict): resulting sudoku in dictionary form.
    """
    # Create a list of potential twins
    potential_twins = [box for box in values.keys() if len(values[box]) == 2]

    # Create an array of tuples (value, unit) that contain the twin pairs
    tuple_array = []

    for unit in unitlist:

        # Create a Counter for boxes that have two items in length
        item_count = Counter()

        # Search through boxes in each unit
        for box in unit:
            if box in potential_twins:
                item_count[values[box]] += 1

        # Iterate through boxes with 2 nunmbers inside of them
        for key in item_count.keys():
            if item_count[key] == 2:
                tuple_array.append((key, unit))

    # Remove numbers in naked twins from the peers
    for tup in tuple_array:
        key = tup[0]
        unit = tup[1]

        for box in unit:
            if values[box] != key:
                    assign_value(values, box, values[box].replace(key[0], '').replace(key[1], ''))

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    box_dict = {}
    for idx, box in enumerate(boxes):
        if grid[idx] == '.':
            assign_value(box_dict, box, '123456789')
        else:
            assign_value(box_dict, box, grid[idx])

    return box_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)

def eliminate(values):
    """
    Remove the solved boxes value from its peers
    Args:
        values(dict): sudoku in dictionary form.
    Returns:
        values(dict): resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    """
    Set the value of boxes that can only be one value in relation to other boxes in the unit
    Args:
        values(dict): A sudoku in dictionary form.
    Returns:
        values(dict): The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789': 
            dplaces = [box for box in unit if digit in values[box]]           
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """ 
    Iterate eliminate(), naked_twins() and only_choice() to eliminate uncertain boxes

    Args:
        values(dict): sudoku in dictionary form.
    Returns:
        values(dict): resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Using depth-first search and constraint propagation, try all possible values.
    Args:
        values(dict): sudoku in dictionary form.
    Returns:
        resulting sudoku in dictionary form if successful, otherwise return False
    """
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values

    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        resulting sudoku in dictionary form if successful, otherwise return False
    """
    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

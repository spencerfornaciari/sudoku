# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propagation is the concept of using limitations to reduce the number of choices we have, in the case of the naked twin problem we know that since there are two boxes with the same value, only those squares are able to contain them. Using this limitation we are able to reduce the number of other choices by removing those numbers from the remaining boxes that exist in their units.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Constraint propagation is a little bit different in the case of diagonal units since each box belongs to different row and column than every other box in the diagonal. Fundamentally though it follows the same restrictions as any other unit in Sudoku (only one value between 1-9 for each box in any given unit). Given this I added the diagonal boxes to our unit list so it would check for our existing constraints (elimination, only choice and naked twins) in the diagonals just like the other units. Since diagonals provide another source of information for our search through the units, it helps expedite the speed at which we're able to solve the puzzle as it increases the knowledge of a box as the number of peers for a box are increased (horizontal, vertical, 3x3 grid, and diagonal).
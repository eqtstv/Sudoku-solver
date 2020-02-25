import time
import grids

def print_grid(arr):
    array = [list(map(str, x)) for x in arr]

    for i in range(9):
        print("{} | {} | {}".format(" ".join(array[i][0:3]), " ".join(array[i][3:6]), " ".join(array[i][6:9])))
    
        if i == 2 or i == 5:
            print("---------------------")            

def find_empty_location(array):
    """Find unasigned location, return coorditates if exist, else return False"""
    for row in range(9):
        for col in range(9):
            if(array[row][col] == 0):
                return row, col
    return False

def used_in_row(array, row, num):
    return num in array[row]

def used_in_col(array, col, num):
    for row in range(9):
        if(array[row][col] == num):
            return True
    return False

def used_in_box(array, row, col, num):
    boxx = row - row%3
    boxxy = col - col%3
    for row in range(3):
        for col in range(3):
            if(array[row+boxx][col+boxxy] == num):
                return True
    return False

def valid_location(array, row, col, num):
    return not (used_in_row(array,row,num) or used_in_col(array,col,num) or  used_in_box(array,row, col, num))

def solve_sudoku(array):
    if not find_empty_location(array):
        return True

    row, col = find_empty_location(array)

    for num in range(1, 10):
        if(valid_location(array, row, col, num)):
            array[row][col] = num

            if(solve_sudoku(array)):
                return True

            array[row][col] = 0

    return False


grid = grids.grid

print_grid(grid)

start_time = time.time()
if solve_sudoku(grid):
    print("\n")
    print("Solved sudoku:")
    print_grid(grid)
    print("\n")
    print("Solved in: %s seconds" % (round(time.time() - start_time, 4)))
else:
    print("No solution exists")
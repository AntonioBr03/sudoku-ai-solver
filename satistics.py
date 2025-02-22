import pygame
import random
import time

WIDTH = 800
backColor = (251, 247, 245)
CELL_SIZE = 50
BUTTON_WIDTH = 80  
BUTTON_HEIGHT = 15  
BUTTON_MARGIN = 50

backtracks = 0
recursions = 0

def generate_sudoku():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    original_numbers = [[False for _ in range(9)] for _ in range(9)]
    for i in range(0, 9, 3):
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(nums)
        for j in range(3):
            for k in range(3):
                grid[i + j][i + k] = nums.pop()

    solve_sudoku(grid)
    remove_numbers(grid, 50)
    for i in range(9):
        for j in range(9):
            original_numbers[i][j] = grid[i][j] != 0
    return grid, original_numbers

def remove_numbers(grid, num_to_remove):
    for _ in range(num_to_remove):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while grid[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        grid[row][col] = 0

def solve_sudoku(grid):
    find = find_empty_location(grid)
    if not find:
        return True
    row, col = find

    for num in range(1, 10):
        if is_a_valid_move_csp(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0
    return False

def find_empty_location(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

def is_a_valid_move_csp(grid, row, col, number):
    for x in range(9):
        if grid[row][x] == number or grid[x][col] == number:
            return False
    corner_row, corner_col = row - row % 3, col - col % 3
    for x in range(3):
        for y in range(3):
            if grid[corner_row + x][corner_col + y] == number:
                return False
    return True

def count_legal_values(grid, row, col):
    if grid[row][col] != 0:
        return 0
    return sum(is_a_valid_move_csp(grid, row, col, num) for num in range(1, 10))

def find_mrv_cell(grid):
    min_count = 10
    min_cell = (-1, -1)
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                count = count_legal_values(grid, row, col)
                if count < min_count:
                    min_count = count
                    min_cell = (row, col)
    return min_cell

def csp_solve(grid, original_numbers, row, col, depth=0):
    global backtracks, recursions
    recursions += 1
    if col == 9:
        if row == 8:
            return True
        row, col = row + 1, 0
    if grid[row][col] > 0:
        return csp_solve(grid, original_numbers, row, col + 1, depth + 1)
    for num in range(1, 10):
        if is_a_valid_move_csp(grid, row, col, num):
            grid[row][col] = num
            if csp_solve(grid, original_numbers, row, col + 1, depth + 1):
                return True
            grid[row][col] = 0
            backtracks += 1
    return False

def csp_solve_mrv(grid, original_numbers, depth=0):
    global backtracks, recursions
    recursions += 1
    row, col = find_mrv_cell(grid)
    if (row, col) == (-1, -1):
        return True
    for num in range(1, 10):
        if is_a_valid_move_csp(grid, row, col, num):
            grid[row][col] = num
            if csp_solve_mrv(grid, original_numbers, depth + 1):
                return True
            grid[row][col] = 0
            backtracks += 1
    return False

def count_common_candidates(grid, row, col):
    if grid[row][col] != 0:
        return 0
    common_candidates = 0
    peers = get_peers(row, col)
    for peer_row, peer_col in peers:
        for num in range(1, 10):
            if is_a_valid_move_csp(grid, peer_row, peer_col, num) and is_a_valid_move_csp(grid, row, col, num):
                common_candidates += 1
    return common_candidates

def get_peers(row, col):
    peers = set()
    for i in range(9):
        peers.add((row, i))
        peers.add((i, col))
    corner_row, corner_col = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            peers.add((corner_row + i, corner_col + j))
    peers.remove((row, col))
    return list(peers)

def select_cell_ctn(grid, potential_cells_list):
    selected_cell = None
    max_ctn = -1
    for row, col in potential_cells_list:
        ctn = count_common_candidates(grid, row, col)
        if ctn > max_ctn:
            selected_cell = (row, col)
            max_ctn = ctn
    return selected_cell

def csp_solve_mrv_plus(grid, original_grid, depth=0):
    global backtracks, recursions
    recursions += 1
    
    def count_legal_values(grid, row, col):
        if grid[row][col] != 0:
            return 0
        return sum(is_a_valid_move_csp(grid, row, col, num) for num in range(1, 10))

    def find_mrv_cells(grid):
        min_count = 10
        mrv_cells = []
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    count = count_legal_values(grid, row, col)
                    if count < min_count:
                        min_count = count
                        mrv_cells = [(row, col)]
                    elif count == min_count:
                        mrv_cells.append((row, col))
        return mrv_cells

    def select_unassigned_variable(grid):
        mrv_cells = find_mrv_cells(grid)
        if not mrv_cells:
            return None
        if len(mrv_cells) == 1:
            return mrv_cells[0]
        return select_cell_ctn(grid, mrv_cells)

    cell = select_unassigned_variable(grid)
    if cell is None:
        return True
    row, col = cell

    for num in range(1, 10):
        if is_a_valid_move_csp(grid, row, col, num):
            grid[row][col] = num
            if csp_solve_mrv_plus(grid, original_grid, depth + 1):
                return True
            grid[row][col] = 0
            backtracks += 1
    return False

def generate_puzzles(difficulty, num_puzzles):
    puzzles = []
    for _ in range(num_puzzles):
        grid = [[0 for _ in range(9)] for _ in range(9)]
        original_numbers = [[False for _ in range(9)] for _ in range(9)]
        for i in range(0, 9, 3):
            nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            random.shuffle(nums)
            for j in range(3):
                for k in range(3):
                    grid[i + j][i + k] = nums.pop()

        solve_sudoku(grid)
        
        if difficulty == "easy":
            remove_numbers(grid, random.randint(10, 25))
        elif difficulty == "medium":
            remove_numbers(grid, random.randint(26, 40))
        elif difficulty == "hard":
            remove_numbers(grid, random.randint(41, 55))
        elif difficulty == "godlike":
            remove_numbers(grid, random.randint(56, 70))
        else:
            raise ValueError("Invalid difficulty level")
        
        for i in range(9):
            for j in range(9):
                original_numbers[i][j] = grid[i][j] != 0
        
        puzzles.append((grid, original_numbers))
    
    return puzzles

def run_experiment(difficulty, num_puzzles):
    global backtracks, recursions
    puzzles = generate_puzzles(difficulty, num_puzzles)

    csp_backtracks = []
    mrv_backtracks = []
    mrv_plus_backtracks = []

    csp_recursions = []
    mrv_recursions = []
    mrv_plus_recursions = []

    for grid, original_numbers in puzzles:
        backtracks = 0
        recursions = 0
        csp_solve([row[:] for row in grid], original_numbers, 0, 0)
        print(f"csp {difficulty}: {csp_backtracks}")
        csp_backtracks.append(backtracks)
        csp_recursions.append(recursions)
        
        backtracks = 0
        recursions = 0
        csp_solve_mrv([row[:] for row in grid], original_numbers)
        print(f" mrv {difficulty}: {mrv_backtracks}")
        mrv_backtracks.append(backtracks)
        mrv_recursions.append(recursions)
        
        backtracks = 0
        recursions = 0
        csp_solve_mrv_plus([row[:] for row in grid], original_numbers)
        print(f"mrv+ {difficulty}: {mrv_plus_backtracks}")
        mrv_plus_backtracks.append(backtracks)
        mrv_plus_recursions.append(recursions)

    print(f"Results for {difficulty} puzzles:")
    print(f"Average backtracks for CSP: {sum(csp_backtracks) / num_puzzles}")
    print(f"Average backtracks for MRV: {sum(mrv_backtracks) / num_puzzles}")
    print(f"Average backtracks for MRV+: {sum(mrv_plus_backtracks) / num_puzzles}")
    
    print(f"Average recursions for CSP: {sum(csp_recursions) / num_puzzles}")
    print(f"Average recursions for MRV: {sum(mrv_recursions) / num_puzzles}")
    print(f"Average recursions for MRV+: {sum(mrv_plus_recursions) / num_puzzles}")

if __name__ == "__main__":
    difficulties = ["easy", "medium", "hard", "godlike"]
    num_puzzles = 100
    
    for difficulty in difficulties:
        run_experiment(difficulty, num_puzzles)
import pygame
import random
import time

WIDTH = 800
backColor = (251, 247, 245)
CELL_SIZE = 50
BUTTON_WIDTH = 80  
BUTTON_HEIGHT = 15  
BUTTON_MARGIN = 50
backtracks=0

# Generate Sudoku puzzle
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

# Remove a specific number of cells from the Sudoku grid
def remove_numbers(grid, num_to_remove):
    for _ in range(num_to_remove):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while grid[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        grid[row][col] = 0

# Solve the Sudoku puzzle using backtracking
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
def draw_grid(window):
    for i in range(0, 10):
        if (i % 3 == 0):
            pygame.draw.line(window, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 4)
            pygame.draw.line(window, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 4)

        pygame.draw.line(window, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
        pygame.draw.line(window, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)


def draw_numbers(window, font, grid, original_numbers):
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                if isinstance(grid[i][j], int):
                    if grid[i][j] == 0:
                        color = (0, 0, 0)
                    elif original_numbers[i][j]:
                        color = (0, 0, 255)
                    else:
                        color = (0, 0, 0)
                    text = font.render(str(grid[i][j]), True, color)
                    window.blit(text, (50 * j + 70, 50 * i + 50))
                else:
                    color = (0, 0, 255)
                    text = font.render(str(grid[i][j]), True, color)
                    window.blit(text, (50 * j + 70, 50 * i + 50))
                    

# Find the next empty location in the grid
def find_empty_location(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

# Draw the Sudoku grid and numbers
def draw(window, font, grid, original_numbers):
    window.fill(backColor)
    for i in range(10):
        line_width = 4 if i % 3 == 0 else 2
        pygame.draw.line(window, (0, 0, 0), (50 + CELL_SIZE * i, 50), (50 + CELL_SIZE * i, 500), line_width)
        pygame.draw.line(window, (0, 0, 0), (50, 50 + CELL_SIZE * i), (500, 50 + CELL_SIZE * i), line_width)
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                color = (0, 0, 255) if original_numbers[i][j] else (0, 0, 0)
                text = font.render(str(grid[i][j]), True, color)
                text_rect = text.get_rect(center=(CELL_SIZE * j + 75, CELL_SIZE * i + 75))
                window.blit(text, text_rect)
    draw_button(window, font)

# Draw buttons on the right side of the window
def draw_button(window, font):
    shuffle_text = font.render("Shuffle", True, (0, 0, 0))
    shuffle_text_rect = shuffle_text.get_rect(topright=(650, 60))
    draw_custom_button(window, shuffle_text, shuffle_text_rect)
    
    csp_text= font.render("CSP", True, (0,0,0))
    csp_text_rect=csp_text.get_rect(topleft=(520,120))
    draw_custom_button(window,csp_text,csp_text_rect)

    mrv_text = font.render("MRV", True, (0, 0, 0))
    mrv_text_rect = mrv_text.get_rect(topleft=(520, 180))
    draw_custom_button(window, mrv_text, mrv_text_rect)

    mrv_plus_text = font.render("MRV+", True, (0, 0, 0))
    mrv_plus_text_rect = mrv_plus_text.get_rect(topleft=(520, 240))
    draw_custom_button(window, mrv_plus_text, mrv_plus_text_rect)

    clear_text = font.render("Clear Input", True, (0, 0, 0))
    clear_text_rect = clear_text.get_rect(topleft=(520, 300))
    draw_custom_button(window, clear_text, clear_text_rect)

def draw_custom_button(window, text, text_rect):
    pygame.draw.rect(window, (0, 0, 0), text_rect, 2)

    background_rect = pygame.Rect(text_rect.left, text_rect.top, text_rect.width, text_rect.height)
    pygame.draw.rect(window, (255, 255, 255), background_rect)

    outer_rect = pygame.Rect(text_rect.left - 2, text_rect.top - 2, text_rect.width + 4, text_rect.height + 4)
    pygame.draw.rect(window, (100, 100, 100), outer_rect)

    inner_rect = pygame.Rect(text_rect.left, text_rect.top, text_rect.width, text_rect.height)
    pygame.draw.rect(window, (255, 255, 255), inner_rect)

    window.blit(text, text_rect)

# Validate a move in the Sudoku puzzle
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

# Count legal values
def count_legal_values(grid, row, col):
    if grid[row][col] != 0:
        return 0
    return sum(is_a_valid_move_csp(grid, row, col, num) for num in range(1, 10))

# Find cell with Minimum Remaining Values
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

# CSP solver using simple backtracking
def csp_solve(grid, original_grid, row, col, window, font, original_numbers):
    global backtracks
    if col == 9:
        if row == 8:
            print(f"Number of backtracks (csp): {backtracks}")
            backtracks=0
            return True
        row, col = row + 1, 0
    if grid[row][col] > 0:
        return csp_solve(grid, original_grid, row, col + 1, window, font, original_numbers)
    for num in range(1, 10):
        if is_a_valid_move_csp(grid, row, col, num):
            grid[row][col] = num
            draw(window, font, grid, original_numbers)
            pygame.display.update()
            pygame.time.delay(10)
            if csp_solve(grid, original_grid, row, col + 1, window, font, original_numbers):
                return True
            grid[row][col] = 0
            backtracks+=1
            draw(window, font, grid, original_numbers)
            pygame.display.update()
            pygame.time.delay(10)
    return False


# CSP solver using MRV
def csp_solve_mrv(grid, original_grid, window, font, original_numbers):
    global backtracks
    row, col = find_mrv_cell(grid)
    if (row, col) == (-1, -1):
        print(f"Number of backtracks (mrv): {backtracks}")
        backtracks=0
        return True
    for num in range(1, 10):
        if is_a_valid_move_csp(grid, row, col, num):
            grid[row][col] = num
            draw(window, font, grid, original_numbers)
            pygame.display.update()
            pygame.time.delay(10)
            if csp_solve_mrv(grid, original_grid, window, font, original_numbers):
                return True
            grid[row][col] = 0
            backtracks+=1
            draw(window, font, grid, original_numbers)
            pygame.display.update()
            pygame.time.delay(10)
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

def fog_resolver(grid, potential_cells_list):
    selected_cell = None
    ctn_of_selected_cell = 0

    for row, col in potential_cells_list:
        ctn = 0
        peers = get_peers(row, col)
        for peer_row, peer_col in peers:
            if grid[peer_row][peer_col] == 0:
                for num in range(1,10):
                    if is_a_valid_move_csp(grid, peer_row, peer_col, num) and is_a_valid_move_csp(grid, row, col, num):
                        ctn += 1

        if ctn > ctn_of_selected_cell:
            selected_cell = (row, col)
            ctn_of_selected_cell = ctn

    return selected_cell

# MRV+ solver using CtN heuristic
def csp_solve_mrv_plus(grid, original_grid, window, font, original_numbers):
    global backtracks

    cell = select_unassigned_variable(grid)
    if cell is None:
        print(f"Number of backtracks (MRV+): {backtracks}")
        backtracks = 0
        return True
    row, col = cell

    for num in range(1, 10):
        if is_a_valid_move_csp(grid, row, col, num):
            grid[row][col] = num
            draw(window, font, grid, original_numbers)
            pygame.display.update()
            pygame.time.delay(10)
            if csp_solve_mrv_plus(grid, original_grid, window, font, original_numbers):
                return True
            grid[row][col] = 0
            backtracks += 1
            draw(window, font, grid, original_numbers)
            pygame.display.update()
            pygame.time.delay(10)
    return False

def select_unassigned_variable(grid):
    mrv_cells = find_mrv_plus_cells(grid)
    if not mrv_cells:
        return None
    if len(mrv_cells) == 1:
        return mrv_cells[0]
    return select_cell_ctn(grid, mrv_cells)

def find_mrv_plus_cells(grid):
    min_count = 10
    mrv_cells = []
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                count = sum(is_a_valid_move_csp(grid, row, col, num) for num in range(1, 10))
                if count < min_count:
                    min_count = count
                    mrv_cells = [(row, col)]
                elif count == min_count:
                    mrv_cells.append((row, col))
    return mrv_cells

def select_cell_ctn(grid, potential_cells_list):
    selected_cell = None
    max_ctn = -1
    for row, col in potential_cells_list:
        ctn = sum(
            is_a_valid_move_csp(grid, peer_row, peer_col, num) and is_a_valid_move_csp(grid, row, col, num)
            for peer_row, peer_col in get_peers(row, col)
            for num in range(1, 10)
        )
        if ctn > max_ctn:
            selected_cell = (row, col)
            max_ctn = ctn
    return selected_cell




# Clear user input from the Sudoku grid
def clear_user_input(grid, original_numbers):
    for i in range(9):
        for j in range(9):
            if not original_numbers[i][j]:
                grid[i][j] = 0
                
                              
                

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, WIDTH-100))
    pygame.display.set_caption("Sudoku puzzle")
    window.fill(backColor)
    font = pygame.font.SysFont('Comic Sans MS', 35)

    sudoku_grid, original_numbers = generate_sudoku()
    draw_grid(window)
    draw_numbers(window, font, sudoku_grid, original_numbers)
    draw_button(window, font)
    pygame.display.update()

    selected = None
    csp_mode = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = (pos[1] - 50) // 50
                col = (pos[0] - 50) // 50

                if 530 <= pos[0] <= 650 and 50 <= pos[1] <= 90:
                    
                    sudoku_grid, original_numbers = generate_sudoku()
                    draw_grid(window)
                    draw_numbers(window, font, sudoku_grid, original_numbers)
                    draw_button(window, font)
                    pygame.display.update()

                elif 530 <= pos[0] <= 650 and 120 <= pos[1] <= 160:
                    csp_mode = not csp_mode
                    if csp_mode:
                        original_grid = [row[:] for row in sudoku_grid]
                        csp_solve(sudoku_grid, original_grid, 0, 0, window, font, original_numbers)
                    else:
                        steps = 0
                        csp_mode = False

                elif 530 <= pos[0] <= 650 and 180 <= pos[1] <= 220:
                    original_grid = [row[:] for row in sudoku_grid]
                    csp_solve_mrv(sudoku_grid, original_grid, window, font, original_numbers)

                elif 530 <= pos[0] <= 650 and 240 <= pos[1] <= 280:
                    original_grid = [row[:] for row in sudoku_grid]
                    csp_solve_mrv_plus(sudoku_grid, original_grid, window, font, original_numbers)

                elif 530 <= pos[0] <= 650 and 300 <= pos[1] <= 340:
                    clear_user_input(sudoku_grid, original_numbers)
                    draw_grid(window)
                    draw_numbers(window, font, sudoku_grid, original_numbers)
                    draw_button(window, font)
                    pygame.display.update()

                elif 0 <= row < 9 and 0 <= col < 9 and not original_numbers[row][col]:
                    selected = (row, col)

            if event.type == pygame.KEYDOWN:
                if selected is not None:
                    row, col = selected
                    if event.key == pygame.K_BACKSPACE:
                        sudoku_grid[row][col] = 0
                    elif event.unicode.isdigit():
                        num = int(event.unicode)
                        if 1 <= num <= 9:
                            sudoku_grid[row][col] = num

        window.fill(backColor)
        draw_grid(window)
        draw_numbers(window, font, sudoku_grid, original_numbers)
        draw_button(window, font)
        pygame.display.update()

if __name__ == "__main__":
    main()

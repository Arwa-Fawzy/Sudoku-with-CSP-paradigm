import pygame
import random

pygame.font.init()

screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Sudoku Using CSP")

font1 = pygame.font.SysFont("comicsans", 20)

grid = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

def draw_grid(title, matrix, offset_x):
    pygame.draw.rect(screen, (255, 200, 200), (offset_x, 100, 350, 600))

    text = font1.render(title, 1, (0, 0, 0))
    text_rect = text.get_rect(center=(offset_x + 350 // 2, 500))
    screen.blit(text, text_rect)

    cell_size = 350 // 9
    for i in range(9):
        for j in range(9):
            color = (255, 255, 255) if matrix[i][j] == 0 else (200, 200, 255)
            pygame.draw.rect(screen, color, (offset_x + j * cell_size, i * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, (0, 0, 0), (offset_x + j * cell_size, i * cell_size, cell_size, cell_size), 2)
            if matrix[i][j] != 0:
                num_text = font1.render(str(matrix[i][j]), 1, (0, 0, 0))
                num_rect = num_text.get_rect(center=(offset_x + j * cell_size + cell_size // 2, i * cell_size + cell_size // 2))
                screen.blit(num_text, num_rect)

def is_valid(grid, num, pos):
    for i in range(9):
        if grid[pos[0]][i] == num or grid[i][pos[1]] == num:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if grid[i][j] == num:
                return False

    return True

def find_empty(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

def possible_values(grid, pos):
    row, col = pos
    domain = set(range(1, 10))

    for i in range(9):
        if grid[row][i] != 0:
            domain.discard(grid[row][i])
        if grid[i][col] != 0:
            domain.discard(grid[i][col])

    box_x, box_y = col // 3, row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if grid[i][j] != 0:
                domain.discard(grid[i][j])

    return len(domain)

def find_best_empty(grid):
    empty_cells = [(i, j) for i in range(9) for j in range(9) if grid[i][j] == 0]
    empty_cells.sort(key=lambda pos: possible_values(grid, pos))
    return empty_cells[0] if empty_cells else None

def solve_csp(grid):
    empty = find_best_empty(grid)
    if not empty:
        return True

    row, col = empty

    domain = list(range(1, 10))
    random.shuffle(domain)

    for num in domain:
        if is_valid(grid, num, (row, col)):
            grid[row][col] = num
            screen.fill((255, 200, 200))
            draw_grid("Solving...", grid, 100)
            pygame.display.update()
            pygame.time.delay(100)

            if solve_csp(grid):
                return True

            grid[row][col] = 0
            screen.fill((255, 200, 200))
            draw_grid("Solving...", grid, 100)
            pygame.display.update()
            pygame.time.delay(100)

    return False

run = True
while run:
    screen.fill((255, 200, 200))

    draw_grid("Initial State", grid, 100)
    pygame.display.update()
    pygame.time.delay(2000)

    solve_csp(grid)

    screen.fill((255, 200, 200))

    draw_grid("Final State", grid, 600)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.time.delay(5000)

pygame.quit()

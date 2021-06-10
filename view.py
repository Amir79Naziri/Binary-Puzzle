import pygame


def update_puzzle(puzzle, var):
    changed = []
    if var.gtype == 'row':
        for i in range(len(var.value)):
            if puzzle[var.place][i] == '-':
                changed.append(True)
            else:
                changed.append(False)
            puzzle[var.place][i] = var.value[i]
    else:
        for i in range(len(var.value)):
            if puzzle[i][var.place] == '-':
                changed.append(True)
            else:
                changed.append(False)
            puzzle[:, var.place][i] = var.value[i]
    return changed


def redraw_window(window, puzzle, changed, gtype, place):
    window.fill((82, 182, 154))

    def draw_on_puzzle(win, _i, _j, color, number):
        pygame.draw.rect(win, color, (_i * 50, _j * 50, 50, 50))
        font = pygame.font.SysFont("Calibri", 29, bold=True)
        text_surf = font.render(number, False, (0, 0, 0))
        win.blit(text_surf, (_i * 50 + 20, _j * 50 + 9))

    for i in range(puzzle.shape[0]):
        for j in range(puzzle.shape[1]):
            if gtype == 'row' and i == place:
                if changed[j]:
                    draw_on_puzzle(window, i, j, (19, 46, 31), str(puzzle[i][j]))
                else:
                    draw_on_puzzle(window, i, j, (60, 120, 90), str(puzzle[i][j]))
            elif gtype == 'col' and j == place:
                if changed[i]:
                    draw_on_puzzle(window, i, j, (19, 46, 31), str(puzzle[i][j]))
                else:
                    draw_on_puzzle(window, i, j, (60, 120, 90), str(puzzle[i][j]))
            else:
                draw_on_puzzle(window, i, j, (22, 138, 173), "" if str(puzzle[i][j]) == '-' else str(puzzle[i][j]))

    col_counter = 0
    row_counter = 0

    for i in range(window.get_size()[1] // 50):
        pygame.draw.line(window, (0, 0, 0), (0, col_counter), (window.get_size()[0], col_counter), width=1)
        col_counter += 50

    for j in range(window.get_size()[0] // 50):
        pygame.draw.line(window, (0, 0, 0), (row_counter, 0), (row_counter, window.get_size()[1]), width=1)
        row_counter += 50

    pygame.display.update()


def start(puzzle, values):

    pygame.init()
    clock = pygame.time.Clock()

    window = pygame.display.set_mode((50 * puzzle.shape[1], 50 * puzzle.shape[0]))

    pygame.display.set_caption("Binary Puzzle")
    while len(values) > 0:
        value = values.pop(0)
        changed = update_puzzle(puzzle, value)
        clock.tick(64)
        pygame.time.delay(1500)
        redraw_window(window, puzzle, changed, value.gtype, value.place)

        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                pygame.quit()
                exit(0)

    pygame.time.delay(2500)
    pygame.quit()

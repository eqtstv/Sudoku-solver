# GUI.py
import pygame
import time
pygame.font.init()


class Grid:
    grid=[[0, 3, 0, 0, 1, 0, 0, 6, 0],
          [7, 5, 0, 0, 3, 0, 0, 4, 8],
          [0, 0, 6, 9, 8, 4, 3, 0, 0],
          [0, 0, 3, 0, 0, 0, 8, 0, 0],
          [9, 1, 2, 0, 0, 0, 6, 7, 4],
          [0, 0, 4, 0, 0, 0, 5, 0, 0],
          [0, 0, 1, 6, 7, 5, 2, 0, 0],
          [6, 8, 0, 0, 9, 0, 0, 1, 5],
          [0, 9, 0, 0, 4, 0, 0, 3, 0]]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.grid[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid_location(self.model, row, col, val) and self.solve_sudoku(self.model):
                self.update_model()
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        # Draw Grid Lines
        gap = int(self.width / 9)
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 2
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        if self.selected:
            row, col = self.selected
            if self.cubes[row][col].value == 0:
                self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve_sudoku(self, array):
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

    def solve_gui(self):
        find = find_empty_location(self.model)

        if not find:
            return True

        else:
            row, col = find

        for i in range(1, 10):
            if valid_location(self.model, row, col, i):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)
                pygame.event.pump()

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("Consolas", 38)

        gap = int(self.width / 9)
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (65,105,225))
            win.blit(text, (int(x + (gap/2 - text.get_width()/2)), int(y + (gap/2 - text.get_height()/2))))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (int(x + (gap/2 - text.get_width()/2)), int(y + (gap/2 - text.get_height()/2))))

        if self.selected:
            pygame.draw.rect(win, (65,105,225), (x,y, gap ,gap), 2)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("Consolas", 38)

        gap = int(self.width / 9)
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255,255,255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (int(gap / 2 - text.get_width() / 2)), int(y + (gap / 2 - text.get_height() / 2))))
        if g:
            pygame.draw.rect(win, (124,252,0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (178,34,34), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

def find_empty_location(array):
    for row in range(9):
        for col in range(9):
            if(array[row][col] == 0):
                return row, col
    return False

def valid_location(array, row, col, num):
    def used_in_row(array, row, col, num):
        for i in range(9):
            if(array[row][i] == num and col != i):
                return True
        return False

    def used_in_col(array, row, col, num):
        for i in range(9):
            if(array[i][col] == num and row != i):
                return True
        return False

    def used_in_box(array, row, col, num):
        boxx = row - row%3
        boxxy = col - col%3
        for i in range(3):
            for j in range(3):
                if(array[i+boxx][j+boxxy] == num and (i != row and j !=  col)):
                    return True
        return False
        
    return not (used_in_row(array,row,col,num) or used_in_col(array,row,col,num) or  used_in_box(array,row, col, num))

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


def redraw_window(win, grid, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("Consolas", 30)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 200, 560))
    grid.draw()


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    grid = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    grid.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    grid.solve_gui()

                if event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_RETURN:
                    if grid.selected:
                        i, j = grid.selected
                        if grid.cubes[i][j].temp != 0:
                            grid.place(grid.cubes[i][j].temp)
                                #print("Success")
                                #show success
                            #else:
                                #show("Wrong")
                                #strikes += 1
                            #key = None

                            if grid.is_finished():
                                print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = grid.click(pos)
                if clicked:
                    grid.select(clicked[0], clicked[1])
                    key = None

        if grid.selected and key != None:
            grid.sketch(key)

        redraw_window(win, grid, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
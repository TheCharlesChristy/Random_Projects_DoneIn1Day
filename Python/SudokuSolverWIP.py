import pygame

class SudokuBoard:
    def __init__(self):
        self.cells = [0]*81
        self.possibilities = {} #cellindex : [possible numbers]
        self.generateInitialPossiblities()
    def generateInitialPossiblities(self):
        for i in range(len(self.cells)):
            self.possibilities[i] = [1,2,3,4,5,6,7,8,9]
    
    def Display_Board(self, screen):
        pygame.display.set_caption("Sudoku")
        screen.fill((255, 255, 255))
        pygame.font.init()
        font = pygame.font.Font(None, 16)
        for i in range(len(self.cells)):
            x = i % 9
            y = i // 9
            val = self.cells[i]
            if val == 0 and len(self.possibilities[i]) < 9:
                val = " "
                val_str = self.GenerateString(self.possibilities[i])
                self.blit_multiline_text(screen, val_str, (self.margin + x * 50, self.margin + y * 50), font, (0, 0, 0))
            elif val == 0 and len(self.possibilities[i]) == 9:
                val = " "
            text = font.render(str(val), True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.margin+x * 50 + 25, self.margin + y * 50 + 25))  # Center the text in the cell
            screen.blit(text, text_rect)
            pygame.draw.rect(screen, (0, 0, 0), (x * 50 +self.margin, y * 50+self.margin, 50, 50), 1)  # Draw cell borders
        pygame.draw.rect(screen, (50, 0, 250), (250, 575, 150, 25), 0)
        text = font.render("Solve", True, (255, 255, 255))
        text_rect = text.get_rect(center = (325, 587))
        screen.blit(text, text_rect)
        pygame.display.flip()

    def GenerateString(self, cells):
        retstr = ""
        for i in range(len(cells)):
            cell = cells[i]
            retstr += str(cell)
            retstr += " "
            if i%3 == 2:
                retstr += "\n"
        return retstr
    
    def blit_multiline_text(self, surface, text, pos, font, color):
        words = text.split("\n")  # Split the text by spaces to reassemble with line breaks
        space = font.size(' ')[0]  # Width of a space.
        max_width, max_height = 50, 50  # Maximum cell dimensions
        x, y = pos
        for word in words:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset x to the start of the cell
                y += word_height  # Move y to the next line
            surface.blit(word_surface, (x+10, y))
            x += word_width + space
        return surface



    def setCells(self, cells):
        #cells = {cellindex:cellvalue}
        for cellindex in cells.keys():
            self.cells[cellindex] = int(cells[cellindex])

    def getCellsinRow(self, cellIndex):
        start_of_row = (cellIndex//9)*9
        end_of_row = start_of_row + 9
        cellsinrow = self.cells[start_of_row:end_of_row]
        return cellsinrow
    
    def getCellsinColumn(self, cellIndex):
        cell_indexes = []
        tmp = cellIndex-9
        while tmp >= 0:
            cell_indexes.append(tmp)
            tmp -= 9
        while cellIndex < len(self.cells):
            cell_indexes.append(cellIndex)
            cellIndex += 9
        cell_indexes.sort()
        cells = []
        for i in cell_indexes:
            cells.append(self.cells[i])
        return cells
    
    def getCellsinGroup(self, cellIndex):
        yi = (cellIndex//9) # 0-8
        xi = cellIndex%9
        gyi = yi//3
        gxi = xi//3
        syi = gyi*27
        sxi = gxi*3
        si = syi+sxi
        indexes = [si, si+9, si+18]
        cells_in_group = []
        for index in indexes:
            group_row = self.cells[index:index+3]
            for cell in group_row:
                cells_in_group.append(cell)
        return cells_in_group
    
    def getCollidingCells(self, cellIndex):
        colliding = set()
        for cell in self.getCellsinRow(cellIndex):
            colliding.add(cell)
        for cell in self.getCellsinColumn(cellIndex):
            colliding.add(cell)
        for cell in self.getCellsinGroup(cellIndex):
            colliding.add(cell)
        retarr = []
        for item in colliding:
            retarr.append(int(item))
        return retarr

    
    def SolvePossibities(self):
        self.generateInitialPossiblities()
        for i in range(len(self.cells)):
            cell_possiblities = self.possibilities[i]
            colliding = self.getCollidingCells(i)
            new_possibilities = []
            for possibility in cell_possiblities:
                if possibility not in colliding:
                    new_possibilities.append(possibility)
            if self.cells[i]==0:
                self.possibilities[i] = new_possibilities

    def Solve(self):
        max_steps = 10
        while 0 in self.cells and max_steps > 0:
            self.SolvePossibities()
            for i in range(len(self.cells)):
                if self.cells[i] == 0 and len(self.possibilities[i]) == 1:
                    self.cells[i] = self.possibilities[i][0]
            max_steps -= 1
    
    def Run(self, mode):
        self.margin = 100
        self.screen = pygame.display.set_mode((650, 650))
        running = True
        while running:
            self.Display_Board(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x >= self.margin and x <= 550 and y >= self.margin and y <= 550:
                        x -= self.margin
                        y -= self.margin
                        x = x//50
                        y = y//50
                        cellindex = x + y*9
                        self.cells[cellindex] = (self.cells[cellindex] + 1) % 10
                        self.SolvePossibities()
                    elif x >= 250 and x <= 400 and y >= 575 and y <= 600:
                        if mode == 0: # Traditional Solve
                            self.Solve()
                        else: # Wave Function Collapse Solve
                            self.CollapsePuzzle()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        #get current position of cursor
                        x, y = pygame.mouse.get_pos()
                        if x >= self.margin and x <= 550 and y >= self.margin and y <= 550:
                            x -= self.margin
                            y -= self.margin
                            x = x//50
                            y = y//50
                            cellindex = x + y*9
                            self.cells[cellindex] = (self.cells[cellindex] + 1) % 10
                            self.SolvePossibities()
                        elif x >= 250 and x <= 400 and y >= 575 and y <= 600:
                            if mode == 0: # Traditional Solve
                                self.Solve()
                            else: # Wave Function Collapse Solve
                                self.CollapsePuzzle()
    
    def FindLowestEntropy(self):
        smallest_possibility = [0]*10
        i = 0
        for index in self.possibilities.keys():
            if len(self.possibilities[index]) < len(smallest_possibility) and self.cells[index] == 0:
                smallest_possibility = self.possibilities[index]
                i = index
        return smallest_possibility, i

    def CollapsePuzzle(self):
        # First Solve all possibilities
        max_runs = 10
        while max_runs > 0:
            for i in range(max_runs):
                self.Solve()
            possibilities, index = self.FindLowestEntropy()
            if len(possibilities) == 0:
                return
            self.cells[index] = possibilities[0]
            max_runs -= 1


        



board = SudokuBoard()
board.Run(0)
            
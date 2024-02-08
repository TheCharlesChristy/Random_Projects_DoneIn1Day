import pygame

class Grid:
    def __init__(self, screen, screen_width, screen_height, cell_size, margin):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.margin = margin
        self.grid_width = ((screen_width-2*self.margin) // cell_size) - (1 - (screen_width-2*self.margin) % cell_size)
        self.grid_height = ((screen_height-2*self.margin) // cell_size)  - (1 - (screen_height-2*self.margin) % cell_size)
        self.grid = [0]*(self.grid_width*self.grid_height)

    def draw(self):
        running = True
        self.screen.fill((255,255,255))
        self.DrawGrid()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()

    def IsPrime(self, n):
        if n <= 1:
            return False
        for i in range(2, n//2+1):
            if n % i == 0:
                return False
        return True
    
    def DrawGrid(self):
        surface_width = self.grid_width*self.cell_size
        surface_height = self.grid_height*self.cell_size
        grid_surface = pygame.Surface((surface_width, surface_height))
        grid_surface.fill((255,255,255))
        for row in range(self.grid_height):
            for column in range(self.grid_width):
                if self.IsPrime(self.grid[row*self.grid_width + column]):
                    color = (row*(255//self.grid_width),column*(255//self.grid_height), (row*column)*(255//(self.grid_width*self.grid_height)))
                    rect = pygame.rect.Rect((self.cell_size) * column, (self.cell_size) * row, self.cell_size, self.cell_size)
                    pygame.draw.rect(grid_surface, color, rect)
        # Draw the grid surface to the center of screen
        excess_width = self.screen_width - surface_width
        excess_height = self.screen_height - surface_height
        self.screen.blit(grid_surface, (excess_width//2, excess_height//2))

    def PutValuesInCells(self):
        i = self.grid_width*self.grid_height//2
        di = 1
        dj = -self.grid_width
        n = 1
        while n <= self.grid_width*self.grid_height:
            self.grid[i] = n
            n += 1
            i = i + di
            left_cell = self.grid[i+dj]
            if left_cell == 0:
                di = dj
                if dj == 1:
                    dj = -self.grid_width
                elif dj == -self.grid_width:
                    dj = -1
                elif dj == -1:
                    dj = self.grid_width
                else:
                    dj = 1


            


pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
CELL_SIZE = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
grid = Grid(screen, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, 50)
grid.PutValuesInCells()
grid.draw()
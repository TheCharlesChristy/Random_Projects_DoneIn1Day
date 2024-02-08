import pygame
import math
import random

class cell:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.center = (x + size//2, y + size//2)
        self.pressure = 1
        self.particles = []

    def draw(self, screen, color):
        #pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size), 1)
        pass
    
    def calculate_pressure(self):
        self.pressure = len(self.particles) + 1
        self.pressure = 1/self.pressure
        return self.pressure

class grid:
    def __init__(self, width, height, cellSize):
        self.width = width
        self.height = height
        self.cellSize = cellSize
        self.grid = self.generate_grid()
        self.max_val = 0
        self.min_val = 1

    def generate_grid(self):
        grid = []
        for i in range(self.width*self.height):
            x = (i % self.width) * self.cellSize
            y = (i // self.width) * self.cellSize
            grid.append(cell(x, y, self.cellSize))
        return grid

    def update(self):
        for cell in self.grid:
            cell.calculate_pressure()

    def draw(self, screen):
        for cell in self.grid:
            color = self.get_color(cell.pressure)
            cell.draw(screen, color)

    def get_color(self, value):
        # Calculate expected amount of particles in cell
        if value >= self.max_val:
            self.max_val = value
        if value <= self.min_val:
            self.min_val = value
        if self.max_val == self.min_val:
            return (0, 0, 0)
        # Ensure value is within min and max bounds
        value = max(self.min_val, min(value, self.max_val))
        # Normalize value between 0 and 1
        normalized = (value - self.min_val) / (self.max_val - self.min_val)
        # Interpolate between blue (0, 0, 255) and red (255, 0, 0)
        red = normalized * 255
        blue = (1 - normalized) * 255
        # Construct RGB value
        rgb = (int(red), 0, int(blue))
        
        return rgb
    
    def put_particles_in_cells(self, particles):
        for cell in self.grid:
            cell.particles = []
        for p in particles:
            # convert particle position to grid position
            x = p.position[0] // self.cellSize
            y = p.position[1] // self.cellSize
            # find the cell the particle is in
            cell = self.grid[p.cellid]
            # add particle to cell
            cell.particles.append(p)
            p.cellid = int(x+y*self.width)
    
class Particle:
    def __init__(self, x, y, r):
        self.position = [x, y]
        self.velocity = [0, 0]
        self.radius = r
        self.cellid = -1

    def apply_velocity(self):
        self.position[0] += (self.velocity[0]/100)/substeps
        self.position[1] += (self.velocity[1]/100)/substeps

    def update(self):
        self.checkforcollisions()
        self.checksurroundingcells()
        self.apply_velocity()
        self.checkbounds()

    def checkbounds(self):
        if self.position[0] < self.radius:
            self.position[0] = self.radius
            self.velocity[0] = 0
        if self.position[0] > sim.width - self.radius:
            self.position[0] = sim.width - self.radius
            self.velocity[0] = 0
        if self.position[1] < self.radius:
            self.position[1] = self.radius
            self.velocity[1] = 0
        if self.position[1] > sim.height - self.radius:
            self.position[1] = sim.height-self.radius
            self.velocity[1] = 0

    def checkforcollisions(self):
        cell = sim.grid.grid[self.cellid]
        for particle in cell.particles:
            if particle == self:
                continue
            dx = particle.position[0] - self.position[0]
            dy = particle.position[1] - self.position[1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance < self.radius*2:
                self.position[0] -= (0.5*dx)/substeps
                self.position[1] -= (0.5*dy)/substeps
                #particle.position[0] += 0.5*dx
                #particle.position[1] += 0.5*dy
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.position[0], self.position[1]), self.radius)
    
    def checksurroundingcells(self):
        if self.cellid == -1:
            return
        leftcellid = self.cellid - 1
        rightcellid = self.cellid + 1
        w = (sim.width//sim.CellSize)
        cellstosearch = [leftcellid - w, leftcellid, leftcellid + w, self.cellid - w, self.cellid, self.cellid + w, rightcellid - w, rightcellid, rightcellid + w]
        min_cell_center = [sim.grid.grid[self.cellid].pressure, sim.grid.grid[self.cellid].center]
        for cellid in cellstosearch:
            if cellid < 0 or cellid >= len(sim.grid.grid):
                continue
            cell = sim.grid.grid[cellid]
            if cell.pressure > min_cell_center[0]:
                min_cell_center = [cell.pressure, cell.center]
        
        self.add_velocity_to_center(min_cell_center[1])

    def add_velocity_to_center(self, center):
        self.velocity = [0, 0]
        dx = center[0] - self.position[0]
        dy = center[1] - self.position[1]
        self.velocity[0] += dx
        self.velocity[1] += dy
            

class Sim:
    def __init__(self, w, h, fps):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.particles = []
        self.CellSize = 4*PARTICLE_RADIUS
        self.grid = grid(w//self.CellSize, h//self.CellSize, self.CellSize)
        self.fps = fps

    def update(self):
        self.grid.update()
        self.grid.put_particles_in_cells(self.particles)
        for p in self.particles:
            p.update()
    
    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            for i in range(substeps):
                self.update()
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        pygame.quit()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for p in self.particles:
            p.draw(self.screen)
        frame_rate = str(int(self.clock.get_fps()))
        font = pygame.font.Font(None, 36)
        text = font.render(frame_rate, 1, (255, 255, 255))
        self.grid.draw(self.screen)
        self.screen.blit(text, (10, 10))
        pygame.display.flip()

    def add_particle(self, x, y, r):
        self.particles.append(Particle(x, y, r))

PARTICLE_RADIUS = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BGCOLOR = WHITE
PARTICLE_COLOR = (255-BGCOLOR[0], 255-BGCOLOR[1], 255-BGCOLOR[2])
PARTICLE_COUNT = 100
substeps = 8

pygame.init()
sim = Sim(400, 400, 60)
for i in range(PARTICLE_COUNT):
    sim.add_particle(random.randint(0, 399), random.randint(0, 399), PARTICLE_RADIUS)
sim.run()



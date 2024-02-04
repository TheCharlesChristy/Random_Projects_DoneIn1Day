# The purpose of this sim is to have a bunch of particles that have a random starting position.
# Each particle will interact with nearby particles and try to move away from them.
# Hopefully what will happen is that the particles will spread out and each particle will have a similar amount of space around it.

import random
import pygame
import math

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
PARTICLE_COUNT = 100
PARTICLE_RADIUS = 5
FRAME_RATE = 60
COULOMBS_CONSTANT = 2
# Particle class
class Particle:
    def __init__(self, x, y, radius, id):
        self.position = [x, y] # top left corner of the particle
        self.center = [x + radius, y + radius] # center of the particle
        self.radius = radius
        self.velocity = [0, 0]
        self.acceleration = [0, 0] # Vectors for the win
        self.color = (0, 0, 0)
        self.id = id
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius)

    def update(self, dt, margin):
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt
        if self.position[0] - margin <= 0:
            self.velocity[0] = max(0, self.velocity[0])
        if self.position[0] + 2*self.radius + margin >= SCREEN_WIDTH:
            self.velocity[0] = min(0, self.velocity[0])
        if self.position[1] - margin <= 0:
            self.velocity[1] = max(0, self.velocity[1])
        if self.position[1] + 2*self.radius + margin >= SCREEN_HEIGHT:
            self.velocity[1] = min(0, self.velocity[1])
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.center[0] = self.position[0] + self.radius
        self.center[1] = self.position[1] + self.radius
        absolute_velocity = int(math.sqrt(self.velocity[0]**2 + self.velocity[1]**2))
        self.color = ((absolute_velocity*10)%255, 0, (255-absolute_velocity*10)%255)
        return self.center

class Simulator:
    def __init__(self, width, height, particle_count, particle_radius, frame_rate):
        self.width = width
        self.height = height
        self.margin = 50
        self.grid_width = particle_radius*4
        self.particle_count = particle_count
        self.particle_radius = particle_radius
        self.particles = []
        self.screen = pygame.display.set_mode((width, height))
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = frame_rate
        self.substeps = 20
        self.dt = 1 / (frame_rate * self.substeps)
        self.init_particles()
        self.cells_in_row = int((self.width - self.margin*2) / self.grid_width)
        self.cells_in_col = int((self.height - self.margin*2) / self.grid_width)
        self.grid = [[[] for i in range(self.cells_in_col)] for j in range(self.cells_in_row)]
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.init_particles()
                elif event.key == pygame.K_r:
                    self.particles = []
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    x -= self.margin
                    y -= self.margin
                    if x < 0 or y < 0 or x > self.width - self.margin*2 or y > self.height - self.margin*2:
                        pass
                    else:
                        grid_x = int(x/self.grid_width)
                        grid_y = int(y/self.grid_width)
                        print(self.grid[grid_x][grid_y])


    def init_particles(self):
        for i in range(len(self.particles), len(self.particles) + self.particle_count):
            x = random.randint(self.margin, self.width - self.margin - 2*self.particle_radius)
            y = random.randint(self.margin, self.height - self.margin - 2*self.particle_radius)
            particle = Particle(x, y, self.particle_radius, i)
            self.particles.append(particle)

    def CreateTestParticles(self):
        particle1 = Particle(100, 100, 10, (255, 255, 255), 0)
        particle2 = Particle(120, 100, 10, (255, 255, 255), 1)
        particle3 = Particle(120, 120, 10, (255, 255, 255), 2)
        self.particles.append(particle1)
        self.particles.append(particle2)
        self.particles.append(particle3)

    def update(self):
        for i in range(self.substeps):
            self.update_grid()
            self.update_particles()
    
    def update_grid(self):
        self.grid = [[[] for i in range(self.cells_in_col)] for j in range(self.cells_in_row)]
        for particle in self.particles:
            x = particle.center[0]-self.margin
            y = particle.center[1]-self.margin
            if x < 0 or y < 0 or x > self.width - self.margin*2 or y > self.height - self.margin*2:
                continue
            grid_x = int(x/self.grid_width)
            grid_y = int(y/self.grid_width)
            self.grid[grid_x][grid_y].append(particle)

    def update_particles(self):
        for grid_x in range(len(self.grid)):
            row = self.grid[grid_x]
            for grid_y in range(len(row)):
                cell = row[grid_y]
                for particle in cell:
                    particle.acceleration = [0,0]
                    nearby_particles = self.GetNearbyParticles(grid_x, grid_y)
                    for nearby_particle in nearby_particles:
                        if particle.id == nearby_particle.id:
                            continue
                        dx = (nearby_particle.center[0] - particle.center[0])
                        dy = (nearby_particle.center[1] - particle.center[1])
                        distance = math.sqrt(dx**2 + dy**2)
                        if distance < particle.radius + nearby_particle.radius:
                            overlap = (particle.radius + nearby_particle.radius) - distance
                            particle.position[0] -= (overlap*dx/distance)*self.dt
                            particle.position[1] -= (overlap*dy/distance)*self.dt
                        
                        force = COULOMBS_CONSTANT * (particle.radius * nearby_particle.radius) / (distance**2)
                        angle = math.atan2(dy, dx)
                        
                        force_x = force * math.cos(angle)
                        force_y = force * math.sin(angle)
                        particle.acceleration[0] += force_x
                        particle.acceleration[1] += force_y
                        nearby_particle.acceleration[0] -= force_x
                        nearby_particle.acceleration[1] -= force_y

                        new_center = particle.update(self.dt, self.margin)


    def GetNearbyParticles(self, grid_x, grid_y):
        # Get the particles in the 8 cells around the current cell
        particles = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = grid_x + i
                y = grid_y + j
                if x < 0 or y < 0 or x >= len(self.grid) or y >= len(self.grid[0]):
                    continue
                for particle in self.grid[x][y]:
                    particles.append(particle)
        return particles

    def draw(self):
        self.screen.fill((255, 255, 255))
        for particle in self.particles:
            particle.draw(self.screen)
        pygame.draw.rect(self.screen, (0, 0, 0), (self.margin-10, self.margin-10 , self.width - 2*self.margin + 20, self.height - 2*self.margin+20), 1)
        fps_text = f"FPS: {int(self.clock.get_fps())}"
        font = pygame.font.Font(None, 24)
        text = font.render(fps_text, True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
        pygame.display.flip()

def main():
    pygame.init()
    sim = Simulator(SCREEN_WIDTH, SCREEN_HEIGHT, PARTICLE_COUNT, PARTICLE_RADIUS, FRAME_RATE)
    sim.run()
    pygame.quit()

if __name__ == "__main__":
    main()
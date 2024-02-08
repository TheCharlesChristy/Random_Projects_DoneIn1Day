# The purpose of this sim is to have a bunch of particles that have a random starting position.
# Each particle will interact with nearby particles and try to move away from them.
# Hopefully what will happen is that the particles will spread out and each particle will have a similar amount of space around it.

import random
from HashSpatialGrid import HashSpatialGrid
import pygame
import math

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
MARGIN = 50
SURFACE_WIDTH = SCREEN_WIDTH - 2*MARGIN
SURFACE_HEIGHT = SCREEN_HEIGHT - 2*MARGIN
PARTICLE_COUNT = 1000
PARTICLE_RADIUS = 4
FRAME_RATE = 120
COULOMBS_CONSTANT = 100000
max_velocity = 1
substeps = 2
# Particle class
class Particle:
    def __init__(self, x, y, radius, id):
        self.position = [x, y] # Center of the particle
        self.prev_position = [x, y]
        self.radius = radius
        self.acceleration = [0, 0] # Vectors for the win
        self.color = (0, 0, 0)
        self.id = id
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def Verlet(self, dt):
        # Verlet integration
        temp = self.position
        self.acceleration[0] /= substeps
        self.acceleration[1] /= substeps
        x = 2 * self.position[0] - self.prev_position[0] + self.acceleration[0] * dt * dt
        y = 2 * self.position[1] - self.prev_position[1] + self.acceleration[1] * dt * dt
        self.position[0] = x
        self.position[1] = y
        self.prev_position = temp
        dx = self.position[0] - self.prev_position[0]
        dy = self.position[1] - self.prev_position[1]
        v = math.sqrt(dx**2 + dy**2)
        r = min(255, v*(255/max_velocity))
        self.color = (r, 0, 255-r)
        self.CheckBounds()

    def CheckBounds(self):
        bounds = [0,0,SURFACE_WIDTH,SURFACE_HEIGHT]
        if self.position[0] < bounds[0]:
            l = bounds[0] - self.position[0]
            tmp = self.position[0]
            self.position[0] = bounds[0] + l
            self.prev_position[0] = tmp
        xdistance1 = self.position[0] - bounds[0]
        self.acceleration[0] += (0.1 * COULOMBS_CONSTANT) / (xdistance1**2)
        if self.position[0] > bounds[2]:
            l = self.position[0] - bounds[2]
            tmp = self.position[0]
            self.position[0] = bounds[2] - l
            self.prev_position[0] = tmp
        xdistance2 =  bounds[2] - self.position[0]
        self.acceleration[0] -= (0.1 * COULOMBS_CONSTANT) / (xdistance2**2)
        if self.position[1] < bounds[1]:
            l = bounds[1] - self.position[1]
            tmp = self.position[1]
            self.position[1] = bounds[1] + l
            self.prev_position[1] = tmp
        ydistance1 = self.position[1] - bounds[1]
        self.acceleration[1] = (0.1 * COULOMBS_CONSTANT) / (ydistance1**2)
        if self.position[1] > bounds[3]:
            l = self.position[1] - bounds[3]
            tmp = self.position[1]
            self.position[1] = bounds[3] - l
            self.prev_position[1] = tmp
        ydistance2 = bounds[3] - self.position[1]
        self.acceleration[1] -= (0.1 * COULOMBS_CONSTANT) / (ydistance2**2)
            

    def ApplyForces(self):
        nearby_particles = grid.FindNearby(self.position)
        for particle in nearby_particles:
            if particle.id == self.id:
                continue
            distance = math.sqrt((self.position[0]-particle.position[0])**2 + (self.position[1]-particle.position[1])**2)
            if distance > 0:
                force = COULOMBS_CONSTANT / (distance**2)
                direction = [self.position[0]-particle.position[0], self.position[1]-particle.position[1]]
                self.acceleration[0] += 0.5 * force * direction[0] / distance
                self.acceleration[1] += 0.5 * force * direction[1] / distance
                particle.acceleration[0] -= 0.5 * force * direction[0] / distance
                particle.acceleration[1] -= 0.5 * force * direction[1] / distance
            

    def update(self, dt):
        self.Verlet(dt)
        self.ApplyForces()
        #self.acceleration = [0, 0]

grid = HashSpatialGrid([[0,0], [SURFACE_WIDTH, SURFACE_HEIGHT]], [SURFACE_WIDTH, SURFACE_HEIGHT], PARTICLE_RADIUS)
particles = []
for i in range(PARTICLE_COUNT):
    particles.append(Particle(random.randint(PARTICLE_RADIUS, SURFACE_WIDTH-PARTICLE_RADIUS), random.randint(PARTICLE_RADIUS, SURFACE_HEIGHT-PARTICLE_RADIUS), PARTICLE_RADIUS, i))
grid.AddParticles(particles)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print acceleration of particle at position
            x,y = pygame.mouse.get_pos()
            x -= MARGIN
            y -= MARGIN
            for particle in particles:
                if math.sqrt((particle.position[0]-x)**2 + (particle.position[1]-y)**2) < PARTICLE_RADIUS:
                    print(particle.acceleration)
    screen.fill((255, 255, 255))
    grid.update()
    surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))
    surface.fill((255, 255, 255))
    fps = clock.get_fps()
    if fps == 0:
        fps = FRAME_RATE
    for i in range(substeps):
        for particle in particles:
            particle.update(1/fps)
    for particle in particles:
        particle.draw(surface)
    screen.blit(surface, (MARGIN, MARGIN))
    pygame.display.flip()
    clock.tick(FRAME_RATE)
import pygame
import math
import random
import HashSpatialGrid as HashSpatialGrid

pygame.init()

frame_rate = 60
substeps = 16
screen_height_Meters = 1
time_to_cross_screen = 0.5 #seconds
screen_width = 600
screen_height = 600
bounce_coefficient = 0.8 #percentage of velocity retained after bouncing off of a wall
number_of_particles = 100
particle_size = 7
gravity = (2*screen_height_Meters*screen_height/((frame_rate*time_to_cross_screen)**2))*substeps # rate of change of velocity per frame
maximum_velocity = (2*screen_height_Meters*screen_height/(frame_rate*time_to_cross_screen))*substeps # maximum velocity of a particle

class Particle:
    def __init__(self, id, position, particle_radius, color, gravity):
        self.id = id
        self.position = position
        self.previous_position = [position[0], position[1]]
        self.radius = particle_radius
        self.color = color
        self.acceleration = [0, gravity]


    def update(self, dt, grid):
        nearby_particles = grid.FindNearby(self.position)
        for particle in nearby_particles:
            if particle.id == self.id:
                continue
            else:
                distance = math.sqrt(((self.position[0]-particle.position[0])**2)+((self.position[1]-particle.position[1])**2))
                if distance < particle.radius + self.radius:
                    overlap = (particle.radius + self.radius) - distance
                    
                    dx = self.position[0] - self.previous_position[0]
                    dy = self.position[1] - self.previous_position[1]

                    direction_x = particle.position[0] - self.position[0]
                    direction_y = particle.position[1] - self.position[1]
                    direction_magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
                    if direction_magnitude == 0:
                        pass
                    else:
                        direction_x /= direction_magnitude  # Normalize
                        direction_y /= direction_magnitude  # Normalize
        
                        # Calculate how much to move; you might add a tiny extra to ensure they don't overlap
                        move_distance = overlap
                        # Update the position of one particle (or both, depending on your requirement)
                        # For example, moving 'self' particle away from the 'particle'
                        self.position[0] -= 0.5*((direction_x * move_distance))*dt
                        self.position[1] -= 0.5*((direction_y * move_distance))*dt
                        # And the 'particle' away from 'self'
                        particle.position[0] += 0.5*((direction_x * move_distance))*dt
                        particle.position[1] += 0.5*((direction_y * move_distance))*dt
        self.Solve_Verlet(dt)
        self.checkforwalls(grid)

    def Solve_Verlet(self, dt):
        # Verlet integration
        temp = self.position
        xpos = 2*self.position[0] - self.previous_position[0] + self.acceleration[0]*(1/frame_rate)**2
        ypos = 2*self.position[1] - self.previous_position[1] + self.acceleration[1]*(1/frame_rate)**2
        self.position = [xpos, ypos]
        self.previous_position = temp
    
    def checkforwalls(self, grid):
        #left wall
        dx = self.position[0] - self.previous_position[0]
        dy = self.position[1] - self.previous_position[1]
        if self.position[0] < grid.bounds[0][0]+1:
            self.previous_position[0] = self.position[0]-dx
            self.position[0] = (grid.bounds[0][0]+1) - (bounce_coefficient*dx)
        #right wall
        elif self.position[0] > grid.bounds[1][0]-1:
            self.previous_position[0] = self.position[0]-dx
            self.position[0] = (grid.bounds[1][0]-1) - (bounce_coefficient*dx)
        #top wall
        elif self.position[1] < grid.bounds[0][1]+1:
            self.previous_position[1] = self.position[1]-dy
            self.position[1] = (grid.bounds[0][1]+1) - (bounce_coefficient*dy)
        #bottom wall
        elif self.position[1] > grid.bounds[1][1]-1:
            self.previous_position[1] = self.position[1]-dy
            self.position[1] = (grid.bounds[1][1]-1) - (bounce_coefficient*dy)
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)
                    

class Simulator:
    def __init__(self, bounds, margin, particle_radius, substeps):
        gridbounds = [[bounds[0][0]+margin, bounds[0][1]+margin], [bounds[1][0]-margin, bounds[1][1]-margin]]
        dimensions = [gridbounds[1][0]-gridbounds[0][0], gridbounds[1][1]-gridbounds[0][1]]
        self.grid = HashSpatialGrid.HashSpatialGrid(gridbounds, dimensions, 2*particle_radius)
        self.grid.CheckVariables()
        self.particles = []
        self.substeps = 4
        self.dt = 1/substeps
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
    
    def update(self):
        self.grid.update()
        for particle in self.particles:
            for i in range(self.substeps):
                particle.update(self.dt, self.grid)
    
    def draw(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.grid.bounds[0][0]-particle_size, self.grid.bounds[0][1]-particle_size, self.grid.dimensions[0]+2*particle_size, self.grid.dimensions[1]+2*particle_size), 1)
        for particle in self.particles:
            particle.draw(self.screen)

    def add_particles(self, particles):
        for particle in particles:
            self.particles.append(particle)
        self.grid.AddParticles(particles)

    def run(self):
        running = True
        frames_to_run = -1
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        frames_to_run += 1
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_p:
                        create_particles()
            if frames_to_run > 0 or frames_to_run == -1:
                self.update()
                if frames_to_run > 0:
                    frames_to_run -= 1
            self.draw()
            fps_text = f"FPS: {int(self.clock.get_fps())}"
            font = pygame.font.Font(None, 24)
            text = font.render(fps_text, True, (0, 0, 0))
            self.screen.blit(text, (10, 10))
            pygame.display.flip()
            self.clock.tick(frame_rate)
        pygame.quit()

sim = Simulator([[0, 0], [screen_width, screen_height]], 100, particle_size, substeps)

def create_particles():
    particles = []
    for i in range(len(sim.particles), len(sim.particles)+number_of_particles):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        particles.append(Particle(i, [random.randint(sim.grid.bounds[0][0], sim.grid.bounds[1][0]-1), random.randint(sim.grid.bounds[0][1], sim.grid.bounds[1][1]-1)], particle_size, color, gravity))
    sim.add_particles(particles)

create_particles()

sim.run()
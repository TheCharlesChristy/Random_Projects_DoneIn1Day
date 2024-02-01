import pygame
import math
import random

pygame.init()

frame_rate = 60
time_to_cross_screen = 1.5 #seconds
screen_width = 400
screen_height = 400
bounce_coefficient = 0.1 #percentage of velocity retained after bouncing off of a wall
friction_coefficient = 0.9 #percentage of velocity retained per frame due to friction
minimum_velocity = 0.99 - 2*(screen_height/((frame_rate*time_to_cross_screen)**2)) #minimum velocity before stopping
number_of_particles = 100
particle_size = 3

class Sim:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill((255, 255, 255))
        self.particles = {}

    def addParticle(self, particle):
        self.particles[particle.id] = particle

    def update(self):
        for particle in self.particles.values():
            particle.update()
            particle.draw(self.screen)

    def run(self):
        while True:
            pygame.time.delay(int(1000/frame_rate))
            self.screen.fill((255, 255, 255))
            self.update()
            pygame.display.flip()
            if pygame.event.poll().type == pygame.QUIT:
                break
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                for i in range(len(self.particles.keys()), len(self.particles.keys()) + 50):
                    self.addParticle(Particle(random.randint(0, screen_width), random.randint(0, screen_height-particle_size), particle_size, GetRandomColor(), i))
    
    def CheckForCollision(self, next_position, size, id, velocity):
        for particle in self.particles.values():
            if particle.id != id:
                dx = next_position[0] - particle.position[0]
                dy = next_position[1] - particle.position[1]
                distance = math.sqrt(dx**2 + dy**2)
                if distance == 0:
                    continue
                # Check if particles are colliding
                if distance <= size + particle.size:
                    # Normal and Tangent vectors
                    normal = [dx / distance, dy / distance]
                    tangent = [-normal[1], normal[0]]

                    # Decompose velocities into normal and tangential components
                    dot_product_normal1 = normal[0] * velocity[0] + normal[1] * velocity[1]
                    dot_product_normal2 = normal[0] * particle.velocity[0] + normal[1] * particle.velocity[1]
                    dot_product_tangent1 = tangent[0] * velocity[0] + tangent[1] * velocity[1]
                    dot_product_tangent2 = tangent[0] * particle.velocity[0] + tangent[1] * particle.velocity[1]

                    # New normal velocities (1D elastic collision equations)
                    m1 = size  # Assuming size as mass
                    m2 = particle.size  # Assuming particle.size as mass
                    new_normal_velocity1 = (dot_product_normal1 * (m1 - m2) + 2 * m2 * dot_product_normal2) / (m1 + m2)
                    new_normal_velocity2 = (dot_product_normal2 * (m2 - m1) + 2 * m1 * dot_product_normal1) / (m1 + m2)

                    # Convert the scalar normal and tangential velocities into vectors
                    new_normal_velocity1_vec = [new_normal_velocity1 * normal[0], new_normal_velocity1 * normal[1]]
                    new_normal_velocity2_vec = [new_normal_velocity2 * normal[0], new_normal_velocity2 * normal[1]]
                    tangential_velocity1_vec = [dot_product_tangent1 * tangent[0], dot_product_tangent1 * tangent[1]]
                    tangential_velocity2_vec = [dot_product_tangent2 * tangent[0], dot_product_tangent2 * tangent[1]]

                    # Combine the normal and tangential velocities to get the final velocity
                    final_velocity1 = (new_normal_velocity1_vec[0] + tangential_velocity1_vec[0], new_normal_velocity1_vec[1] + tangential_velocity1_vec[1])
                    final_velocity2 = (new_normal_velocity2_vec[0] + tangential_velocity2_vec[0], new_normal_velocity2_vec[1] + tangential_velocity2_vec[1])

                    # Update velocities
                    particle.SetCollisionVelocity(final_velocity2)

                    # Return the new velocity of the current particle
                    return final_velocity1

        # If no collision, return the original velocity
        return velocity
    
    def GetParticle(self, id):
        return self.particles[id]

class Particle:
    def __init__(self, x, y, size, color, id):
        self.id = id
        self.position = (x, y)
        self.size = size
        self.color = color
        self.velocity = (0, 0)
        self.vmax = 2*(screen_height/(time_to_cross_screen*frame_rate)) # maximum velocity in pixels per frame
        self.deltaV = self.vmax/(time_to_cross_screen*frame_rate) # change in velocity per frame
        self.colliding = False

    def update(self):
        if self.velocity[1] == 0 and self.position[1] == screen_height - self.size:
            self.velocity = (self.velocity[0]*friction_coefficient, 0)
            return
        self.velocity = (self.velocity[0], min(self.velocity[1] + self.deltaV, self.vmax))
        next_position = (self.position[0] + self.velocity[0], min(self.position[1] + self.velocity[1], screen_height - self.size))
        if next_position[0] < 0:
            next_position = (-next_position[0], next_position[1])
            self.velocity = (-bounce_coefficient*self.velocity[0], self.velocity[1]*friction_coefficient)
            if math.fabs(self.velocity[0]) < minimum_velocity:
                self.velocity = (0, self.velocity[1])
            
        elif next_position[0]+self.size > screen_width:
            next_position = (2*screen_width-(next_position[0]+2*self.size), next_position[1])
            self.velocity = (-bounce_coefficient*self.velocity[0], self.velocity[1]*friction_coefficient)
            if math.fabs(self.velocity[0]) < minimum_velocity:
                self.velocity = (0, self.velocity[1])
        
        if next_position[1]+self.size >= screen_height:
            next_position = (next_position[0], 2*screen_height-(next_position[1]+2*self.size))
            self.velocity = (self.velocity[0]*friction_coefficient, -bounce_coefficient*self.velocity[1])
            if math.fabs(self.velocity[1]) < minimum_velocity:
                self.velocity = (self.velocity[0], 0)
        
        self.velocity = sim.CheckForCollision(next_position, self.size, self.id, self.velocity)
            
        next_position = (math.trunc(next_position[0]), math.trunc(next_position[1]))
        self.position = next_position

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.position[0], self.position[1]), self.size)

    def SetCollisionVelocity(self, velocity):
        self.velocity = velocity
    
def GetRandomColor():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))
sim = Sim(screen_width, screen_height)
for i in range(number_of_particles):
    sim.addParticle(Particle(random.randint(0, screen_width), random.randint(0, screen_height-particle_size), particle_size, GetRandomColor(), i))
sim.run()

import pygame
import random
import math
from physics import *

pygame.init()

version = "1.2.0"

scale = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
FPS = 30
dt = clock.tick(FPS) / 1000
sim_speed = 15
dt *= sim_speed

gravity_x = 0
gravity_y = 0
grav_constant = 10

spread_factor = 1.1
repulsion_force = 1.2
collision = True

global_id = -1

class Particle(pygame.sprite.Sprite):
    def __init__(self, position, mass, elasticity, radius):
        super().__init__()
        global global_id

        if elasticity > 1 or elasticity < 0:
            raise ValueError(f"Elasticity value must be between 0 and 1")

        self.x, self.y = position
        self.vx, self.vy = 0, 0

        self.mass = mass
        self.elasticity = elasticity

        self.radius = radius * scale
        self.color = (255, 255, 255)

        global_id += 1
        self.id = global_id

    def handle_collision(self, other=None):
        if other is None:
            # Floor collision
            if self.y + self.radius > SCREEN_HEIGHT:
                self.vy = -self.vy * self.elasticity
                self.y = SCREEN_HEIGHT - self.radius  # push it up slightly
        else:

            dx = other.x - self.x
            dy = other.y - self.y
            distance = math.hypot(dx, dy)

            # Avoid division by zero when particles are exactly overlapping
            if distance == 0:
                # Move particles slightly apart on x-axis (or y-axis)
                distance = 0.001
                dx = 0.001
                dy = 0

            if distance <= ( self.radius * spread_factor) + ( other.radius * spread_factor):
                avg_elasticity = (self.elasticity + other.elasticity) / 2

                self.vx = -self.vx * avg_elasticity * repulsion_force
                self.vy = -self.vy * avg_elasticity * repulsion_force
                other.vx = -other.vx * avg_elasticity * repulsion_force
                other.vy = -other.vy * avg_elasticity * repulsion_force


                overlap = (( self.radius * spread_factor) + ( other.radius * spread_factor)) - distance
                if overlap > 0:
                    nx = dx / distance
                    ny = dy / distance
                    self.x -= nx * overlap / 2
                    self.y -= ny * overlap / 2
                    other.x += nx * overlap / 2
                    other.y += ny * overlap / 2

    def update(self):
        self.vx += gravity_x * dt
        self.vy += gravity_y * dt

        self.x += self.vx * dt
        self.y  += self.vy * dt


    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.radius)

all_particles = []

for i in range(150):
    instance = Particle((random.randint(0,800), random.randint(0,600)), 1, random.uniform(0.1,0.99), 10)
    all_particles.append(instance)

run = True
while run:
    dt = clock.tick(FPS) / 1000
    dt*= sim_speed

    pygame.event.pump()

    SCREEN.fill((0, 0, 0))
    for particle in all_particles:
        particle.update()
        particle.handle_collision()
        particle.draw()

    for i in range(len(all_particles)):
        for j in range(i + 1, len(all_particles)):
            p1 = all_particles[i]
            p2 = all_particles[j]
            p1.fx, p1.fy = 0, 0
            p2.fx, p2.fy = 0, 0

            compute_gravity(p1, p2, grav_constant)
            p1.ax = p1.fx / p1.mass
            p1.ay = p1.fy / p1.mass
            p2.ax = p2.fx / p2.mass
            p2.ay = p2.fy / p2.mass

            p1.vx += p1.ax
            p1.vy += p1.ay
            p2.vx += p2.ax
            p2.vy += p2.ay

            if collision:
                p1.handle_collision(p2)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                instance = Particle(event.pos, 100, random.uniform(0.1, 0.99), random.randint(5, 30))
                all_particles.append(instance)

    pygame.display.flip()

pygame.quit()
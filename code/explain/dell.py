import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Particle System")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Particle class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(19, 20)
        self.color = RED
        self.life = random.randint(50, 100)
        self.x_velocity = random.uniform(-2, 2)
        self.y_velocity = random.uniform(-2, 2)

    def update(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.life -= 1
        self.size -= 0.1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# Create a list to hold particles
particles = []

# Main loop
running = True
while running:
    screen.fill(BLACK)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Add new particles to the list
    if random.random() < 2:
        particles.append(Particle(400, 300))  # Start particles at the center of the screen

    # Update and draw particles
    for particle in particles[:]:
        particle.update()
        particle.draw(screen)
        if particle.life <= 0:
            particles.remove(particle)

    # Update the screen
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()

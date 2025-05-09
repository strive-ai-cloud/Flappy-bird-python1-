import pygame
import random
import os
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Font and Clock
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

# Bird settings
bird_x = 60
bird_radius = 20
gravity = 0.4
jump_strength = -8

# Pipe settings
pipe_width = 70
pipe_gap = 170
pipe_speed = 3

# Score setup
score = 0
highscore_file = "highscore.txt"
if os.path.exists(highscore_file):
    with open(highscore_file, "r") as f:
        high_score = int(f.read())
else:
    high_score = 0

# Function to create a pipe
def create_pipe():
    top = random.randint(80, HEIGHT - pipe_gap - 80)
    bottom = top + pipe_gap
    return {"x": WIDTH, "top": top, "bottom": bottom, "scored": False}

# Start screen
def show_start_screen():
    screen.fill(BLUE)
    title = font.render("Vanshu-Flappy Bird Clone", True, BLACK)
    instr = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
    screen.blit(instr, (WIDTH // 2 - instr.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    
    # Wait for space
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
        clock.tick(15)

# Main game loop
def main_game():
    global score, high_score
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    running = True

    while running:
        screen.fill(BLUE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

        # Update bird
        bird_velocity += gravity
        bird_y += bird_velocity

        # Add new pipes
        if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - 200:
            pipes.append(create_pipe())

        # Move and draw pipes
        for pipe in pipes:
            pipe["x"] -= pipe_speed
            pygame.draw.rect(screen, GREEN, (pipe["x"], 0, pipe_width, pipe["top"]))
            pygame.draw.rect(screen, GREEN, (pipe["x"], pipe["bottom"], pipe_width, HEIGHT - pipe["bottom"]))

        # Remove off-screen pipes
        pipes = [p for p in pipes if p["x"] + pipe_width > 0]

        # Collision detection & scoring
        for pipe in pipes:
            if pipe["x"] < bird_x + bird_radius < pipe["x"] + pipe_width:
                if bird_y - bird_radius < pipe["top"] or bird_y + bird_radius > pipe["bottom"]:
                    running = False

            if not pipe["scored"] and pipe["x"] + pipe_width < bird_x:
                score += 1
                pipe["scored"] = True

        # Ground and ceiling collision
        if bird_y - bird_radius <= 0 or bird_y + bird_radius >= HEIGHT:
            running = False

        # Draw bird
        pygame.draw.circle(screen, RED, (bird_x, int(bird_y)), bird_radius)

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        high_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(high_text, (10, 50))

        pygame.display.update()
        clock.tick(60)

    # Update high score
    if score > high_score:
        with open(highscore_file, "w") as f:
            f.write(str(score))

# Run full game
show_start_screen()
main_game()
pygame.quit()

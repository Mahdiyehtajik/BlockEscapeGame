import pygame
import random

# Initial settings
pygame.init()
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Escape the Blocks")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)  # New color for player
ORANGE = (255, 165, 0)  # New color for blocks

# Player settings
player_radius = 25
player_x = width // 2
player_y = height - 2 * player_radius
player_speed = 5

# Block settings
block_size = 50
block_speed = 5
block_list = []

# Scoring
score = 0
font = pygame.font.SysFont("monospace", 35)

# Create new block
def create_block():
    block_x = random.randint(0, width - block_size)
    block_y = -block_size
    block_list.append([block_x, block_y])

# Move blocks
def move_blocks(block_list):
    for block in block_list:
        block[1] += block_speed
    block_list[:] = [block for block in block_list if block[1] < height]

# Detect collision between circle player and rectangular block
def detect_collision(player_x, player_y, block_x, block_y):
    # Calculate centers of circle and rectangle
    circle_center = (player_x, player_y)
    rect_center = (block_x + block_size/2, block_y + block_size/2)
    
    # Calculate distance between centers
    distance = ((circle_center[0] - rect_center[0]) ** 2 + 
                (circle_center[1] - rect_center[1]) ** 2) ** 0.5
    
    # If distance is less than sum of circle radius and half of rectangle's diagonal, collision occurred
    return distance < (player_radius + block_size/2)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > player_radius:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_radius:
        player_x += player_speed

    # Create new blocks
    if random.randint(0, 20) == 0:
        create_block()

    # Move blocks
    move_blocks(block_list)

    # Draw player (as yellow circle)
    pygame.draw.circle(screen, YELLOW, (int(player_x), int(player_y)), player_radius)

    # Draw blocks (as orange rectangles)
    for block in block_list:
        pygame.draw.rect(screen, ORANGE, (block[0], block[1], block_size, block_size))

        # Check for collision
        if detect_collision(player_x, player_y, block[0], block[1]):
            running = False

    # Display score
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(30)

    # Increase score and block speed
    score += 1
    if score % 100 == 0:
        block_speed += 1

pygame.quit()
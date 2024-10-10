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
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player settings
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - 2 * player_size
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

# Detect collision
def detect_collision(player_x, player_y, block_x, block_y):
    if (block_x < player_x < block_x + block_size or block_x < player_x + player_size < block_x + block_size) and \
       (block_y < player_y < block_y + block_size or block_y < player_y + player_size < block_y + block_size):
        return True
    return False

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
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += player_speed

    # Create new blocks
    if random.randint(0, 20) == 0:
        create_block()

    # Move blocks
    move_blocks(block_list)

    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

    # Draw blocks
    for block in block_list:
        pygame.draw.rect(screen, RED, (block[0], block[1], block_size, block_size))

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

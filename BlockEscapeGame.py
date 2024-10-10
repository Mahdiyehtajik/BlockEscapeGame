import pygame
import random
import math

# Initial settings
pygame.init()
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Escape the Missiles")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Player settings
player_radius = 25
player_x = width // 2
player_y = height - 2 * player_radius
player_speed = 5

# Missile settings
missile_width = 20
missile_height = 40
missile_speed = 5
missile_list = []

# Explosion settings
explosion_duration = 30  # frames
explosion_frames = []
max_explosion_radius = 40

# Scoring
score = 0
font = pygame.font.SysFont("monospace", 35)

# Create new missile
def create_missile():
    missile_x = random.randint(0, width - missile_width)
    missile_y = -missile_height
    missile_list.append([missile_x, missile_y])

# Move missiles
def move_missiles(missile_list):
    for missile in missile_list:
        missile[1] += missile_speed
    missile_list[:] = [missile for missile in missile_list if missile[1] < height]

# Draw missile (triangle shape)
def draw_missile(x, y):
    points = [
        (x + missile_width // 2, y),  # Top point
        (x, y + missile_height),      # Bottom left
        (x + missile_width, y + missile_height)  # Bottom right
    ]
    pygame.draw.polygon(screen, ORANGE, points)

# Detect collision between circle player and triangular missile
def detect_collision(player_x, player_y, missile_x, missile_y):
    missile_center_x = missile_x + missile_width // 2
    missile_center_y = missile_y + missile_height // 2
    
    distance = math.sqrt((player_x - missile_center_x) ** 2 + 
                         (player_y - missile_center_y) ** 2)
    
    return distance < (player_radius + missile_width // 2)

# Create explosion animation frames
def create_explosion_frames():
    frames = []
    for i in range(explosion_duration):
        radius = int((i / explosion_duration) * max_explosion_radius)
        frames.append(radius)
    return frames

# Draw explosion
def draw_explosion(x, y, frame):
    radius = explosion_frames[frame]
    pygame.draw.circle(screen, RED, (int(x), int(y)), radius)
    pygame.draw.circle(screen, ORANGE, (int(x), int(y)), int(radius * 0.8))
    pygame.draw.circle(screen, YELLOW, (int(x), int(y)), int(radius * 0.6))

# Game loop
running = True
game_over = False
clock = pygame.time.Clock()
explosion_frame = 0
explosion_pos = None
explosion_frames = create_explosion_frames()

while running:
    screen.fill(BLACK)

    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > player_radius:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_radius:
            player_x += player_speed

        # Create new missiles
        if random.randint(0, 20) == 0:
            create_missile()

        # Move missiles
        move_missiles(missile_list)

        # Draw player
        pygame.draw.circle(screen, YELLOW, (int(player_x), int(player_y)), player_radius)

        # Draw missiles and check collisions
        for missile in missile_list:
            draw_missile(missile[0], missile[1])

            # Check for collision
            if detect_collision(player_x, player_y, missile[0], missile[1]):
                game_over = True
                explosion_pos = (player_x, player_y)
                break

    else:  # Game over - show explosion
        if explosion_frame < explosion_duration:
            draw_explosion(explosion_pos[0], explosion_pos[1], explosion_frame)
            explosion_frame += 1
        else:
            running = False

    # Display score
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(30)

    # Increase score and missile speed
    if not game_over:
        score += 1
        if score % 100 == 0:
            missile_speed += 1

pygame.quit()
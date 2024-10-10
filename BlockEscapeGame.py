import pygame
import random
import math
import time

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

# Text settings
game_font = pygame.font.SysFont("monospace", 35)
game_over_font = pygame.font.SysFont("monospace", 50, bold=True)

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
        (x + missile_width // 2, y),
        (x, y + missile_height),
        (x + missile_width, y + missile_height)
    ]
    pygame.draw.polygon(screen, ORANGE, points)

# Detect collision
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

# Draw game over screen
def draw_game_over(final_score):
    # Game Over text
    game_over_text = game_over_font.render("GAME OVER!!!", True, RED)
    text_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 30))
    screen.blit(game_over_text, text_rect)
    
    # Final score text
    score_text = game_font.render(f"Final Score: {final_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(width // 2, height // 2 + 20))
    screen.blit(score_text, score_rect)

# Game loop
running = True
game_over = False
show_game_over = False
clock = pygame.time.Clock()
explosion_frame = 0
explosion_pos = None
explosion_frames = create_explosion_frames()
score = 0

while running:
    screen.fill(BLACK)

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

        # Create and move missiles
        if random.randint(0, 20) == 0:
            create_missile()
        move_missiles(missile_list)

        # Draw player
        pygame.draw.circle(screen, YELLOW, (int(player_x), int(player_y)), player_radius)

        # Draw missiles and check collisions
        for missile in missile_list:
            draw_missile(missile[0], missile[1])
            if detect_collision(player_x, player_y, missile[0], missile[1]):
                game_over = True
                explosion_pos = (player_x, player_y)
                break

        # Display score
        score_text = game_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        score += 1
        if score % 100 == 0:
            missile_speed += 1

    else:  # Game over state
        if explosion_frame < explosion_duration:
            # Draw explosion animation
            draw_explosion(explosion_pos[0], explosion_pos[1], explosion_frame)
            explosion_frame += 1
        else:
            # Show game over screen
            draw_game_over(score)
            if not show_game_over:
                show_game_over = True
                pygame.display.flip()
                time.sleep(3)  # Show game over screen for 3 seconds
                running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
import pygame
import sys

# Initialize pygame and font
pygame.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Paddle size
paddle_width, paddle_height = 10, 100

# Left paddle position (centered vertically)
left_paddle_x = 10
left_paddle_y = HEIGHT // 2 - paddle_height // 2

# Right paddle position (centered vertically)
right_paddle_x = WIDTH - 10 - paddle_width
right_paddle_y = HEIGHT // 2 - paddle_height // 2

# Ball size and position
Ball_size = 15
ball_x = WIDTH // 2 - Ball_size // 2
ball_y = HEIGHT // 2 - Ball_size // 2
ball_speed_x = 5  # Increased from 3 to 5
ball_speed_y = 5  # Increased from 3 to 5

# Paddle movement speed
paddle_speed = 7  # Increased from 5 to 7

# Scores
left_score = 0
right_score = 0

clock = pygame.time.Clock()  # Frame rate controller

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= paddle_speed
    if keys[pygame.K_s] and left_paddle_y < HEIGHT - paddle_height:
        left_paddle_y += paddle_speed
    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - paddle_height:
        right_paddle_y += paddle_speed

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Bounce off top and bottom edges
    if ball_y <= 0:
        ball_y = 0
        ball_speed_y *= -1
    elif ball_y >= HEIGHT - Ball_size:
        ball_y = HEIGHT - Ball_size
        ball_speed_y *= -1

    # Bounce off left paddle
    if (ball_x <= left_paddle_x + paddle_width and
        left_paddle_y < ball_y + Ball_size and
        ball_y < left_paddle_y + paddle_height and
        ball_speed_x < 0):
        ball_speed_x *= -1
        ball_x = left_paddle_x + paddle_width  # Prevent sticking

    # Bounce off right paddle
    if (ball_x + Ball_size >= right_paddle_x and
        right_paddle_y < ball_y + Ball_size and
        ball_y < right_paddle_y + paddle_height and
        ball_speed_x > 0):
        ball_speed_x *= -1
        ball_x = right_paddle_x - Ball_size  # Prevent sticking

    # Score and reset ball if it goes off-screen horizontally
    if ball_x < 0:
        right_score += 1
        ball_x = WIDTH // 2 - Ball_size // 2
        ball_y = HEIGHT // 2 - Ball_size // 2
        ball_speed_x = 5  # Reset speed with increased value
        ball_speed_y = 5
    elif ball_x > WIDTH:
        left_score += 1
        ball_x = WIDTH // 2 - Ball_size // 2
        ball_y = HEIGHT // 2 - Ball_size // 2
        ball_speed_x = -5
        ball_speed_y = 5

    # Drawing
    screen.fill((0, 0, 0))  # Clear screen
    # Draw paddles
    pygame.draw.rect(screen, (255, 255, 255), (left_paddle_x, left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, (255, 255, 255), (right_paddle_x, right_paddle_y, paddle_width, paddle_height))
    # Draw ball (ellipse)
    pygame.draw.ellipse(screen, (255, 255, 255), (int(ball_x), int(ball_y), Ball_size, Ball_size))
    # Draw scores
    left_score_text = font.render(str(left_score), True, (255, 255, 255))
    right_score_text = font.render(str(right_score), True, (255, 255, 255))
    screen.blit(left_score_text, (WIDTH // 4, 20))
    screen.blit(right_score_text, (WIDTH * 3 // 4, 20))

    # Update display
    pygame.display.flip()

    clock.tick(60)  # Limit FPS to 60
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
BIRD_WIDTH, BIRD_HEIGHT = 80, 60  # Increased size for clearer visibility
GRAVITY = 0.5
JUMP_STRENGTH = -8
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3
FPS = 60

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load images
bird_image_raw = pygame.image.load("bird.png")  # Use local path to bird.png
bird_image = pygame.transform.scale(bird_image_raw, (BIRD_WIDTH, BIRD_HEIGHT))


def create_pipe():
    height = random.randint(50, HEIGHT - PIPE_GAP - 50)
    top_rect = pygame.Rect(WIDTH, 0, PIPE_WIDTH, height)
    bottom_rect = pygame.Rect(WIDTH, height + PIPE_GAP, PIPE_WIDTH, HEIGHT)
    return top_rect, bottom_rect


def draw_bird(y):
    screen.blit(bird_image, (50 - BIRD_WIDTH // 2, int(y) - BIRD_HEIGHT // 2))


def draw_pipes(pipe_list):
    for top, bottom in pipe_list:
        pygame.draw.rect(screen, (0, 200, 0), top)
        pygame.draw.rect(screen, (0, 200, 0), bottom)


def check_collision(y, pipe_list):
    bird_rect = pygame.Rect(50 - BIRD_WIDTH // 2, int(y) - BIRD_HEIGHT // 2, BIRD_WIDTH, BIRD_HEIGHT)
    if y - BIRD_HEIGHT // 2 <= 0 or y + BIRD_HEIGHT // 2 >= HEIGHT:
        return True
    for top, bottom in pipe_list:
        if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
            return True
    return False


def display_score(score):
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))


def display_game_over():
    over_text = font.render("Game Over", True, RED)
    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 50))

    retry_text = font.render("Press R to Replay", True, BLACK)
    screen.blit(retry_text, (WIDTH//2 - retry_text.get_width()//2, HEIGHT//2))


def game_loop():
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    frame_count = 0
    running = True
    game_over = False
    scored_pipes = set()

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_velocity = JUMP_STRENGTH
                elif event.key == pygame.K_r and game_over:
                    game_loop()  # Restart game

        if not game_over:
            bird_velocity += GRAVITY
            bird_y += bird_velocity

            if frame_count % 90 == 0:
                pipes.append(create_pipe())

            for top, bottom in pipes:
                top.x -= PIPE_SPEED
                bottom.x -= PIPE_SPEED

            # Update score if the bird has passed a pipe pair
            for i, (top, bottom) in enumerate(pipes):
                if i not in scored_pipes and top.right < 50:
                    score += 1
                    scored_pipes.add(i)

            # Remove pipes that are off-screen
            pipes = [p for p in pipes if p[0].right > 0]

            draw_bird(bird_y)
            draw_pipes(pipes)
            display_score(score)

            if check_collision(bird_y, pipes):
                game_over = True
        else:
            display_game_over()

        pygame.display.update()
        frame_count += 1

# Start the game
game_loop()

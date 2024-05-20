import pygame
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen setup
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Speeds
paddle_speed = 3
ball_speed = [3, 3]

# Rectangles
paddle_a = pygame.Rect(20, height // 2 - 60, 10, 120)
paddle_b = pygame.Rect(width - 30, height // 2 - 60, 10, 120)
ball = pygame.Rect(width // 2 - 10, height // 2 - 10, 20, 20)

# Function to generate beep sounds
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Generate title theme
def generate_title_theme():
    frequencies = [440, 494, 523, 587, 659, 698, 784, 880]
    wave_data = []
    for f in frequencies:
        sound = generate_beep_sound(f, 0.1)
        wave_data.extend(array('h', sound.get_raw()))
    return pygame.mixer.Sound(buffer=array('h', wave_data))

title_theme = generate_title_theme()

# Sounds
wall_sound = generate_beep_sound(440, 0.1)  # Sound for wall collision
paddle_sound = generate_beep_sound(523.25, 0.1)  # Sound for paddle collision

# Font setup
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
tiny_font = pygame.font.Font(None, 24)

# Game states
MAIN_MENU = "main_menu"
GAME = "game"
CREDITS = "credits"
WINNER = "winner"
state = MAIN_MENU

# Scores
score_a = 0
score_b = 0

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def reset_game():
    global score_a, score_b, ball, paddle_a, paddle_b
    score_a = 0
    score_b = 0
    ball = pygame.Rect(width // 2 - 10, height // 2 - 10, 20, 20)
    paddle_a.topleft = (20, height // 2 - 60)
    paddle_b.topleft = (width - 30, height // 2 - 60)

# Play title theme in loop
title_theme.play(-1)

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == MAIN_MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = GAME
                    title_theme.stop()
                elif event.key == pygame.K_c:
                    state = CREDITS

        elif state == GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = MAIN_MENU
                    title_theme.play(-1)

        elif state == WINNER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    state = MAIN_MENU
                    title_theme.play(-1)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        elif state == CREDITS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = MAIN_MENU

    if state == MAIN_MENU:
        draw_text("Pong", font, white, screen, width // 2, height // 4)
        draw_text("Press Enter to Play", small_font, white, screen, width // 2, height // 2)
        draw_text("Press C for Credits", small_font, white, screen, width // 2, height // 2 + 50)
        draw_text("Made by ChatGPT and Various LLMs", tiny_font, white, screen, width // 2, height - 20)
    
    elif state == GAME:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle_a.top > 0:
            paddle_a.move_ip(0, -paddle_speed)
        if keys[pygame.K_s] and paddle_a.bottom < height:
            paddle_a.move_ip(0, paddle_speed)
        if keys[pygame.K_UP] and paddle_b.top > 0:
            paddle_b.move_ip(0, -paddle_speed)
        if keys[pygame.K_DOWN] and paddle_b.bottom < height:
            paddle_b.move_ip(0, paddle_speed)

        ball.move_ip(ball_speed)

        if ball.top <= 0 or ball.bottom >= height:
            ball_speed[1] = -ball_speed[1]
            wall_sound.play()
        if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
            ball_speed[0] = -ball_speed[0]
            paddle_sound.play()

        if ball.left <= 0:
            score_b += 1
            ball.center = (width // 2, height // 2)
        if ball.right >= width:
            score_a += 1
            ball.center = (width // 2, height // 2)

        pygame.draw.rect(screen, white, paddle_a)
        pygame.draw.rect(screen, white, paddle_b)
        pygame.draw.ellipse(screen, white, ball)

        draw_text(f"{score_a}", font, white, screen, width // 4, 50)
        draw_text(f"{score_b}", font, white, screen, 3 * width // 4, 50)

        if score_a >= 5 or score_b >= 5:
            state = WINNER

    elif state == WINNER:
        winner_text = "Player A Wins!" if score_a >= 5 else "Player B Wins!"
        draw_text(winner_text, font, white, screen, width // 2, height // 2 - 50)
        draw_text("Press SPACE to Restart", small_font, white, screen, width // 2, height // 2)
        draw_text("Press ESC to Quit", small_font, white, screen, width // 2, height // 2 + 50)

    elif state == CREDITS:
        draw_text("Credits", font, white, screen, width // 2, height // 4)
        draw_text("Game developed by CatDevZSH", small_font, white, screen, width // 2, height // 2)
        draw_text("Press ESC to return to Main Menu", small_font, white, screen, width // 2, height // 2 + 50)
        draw_text("Made by ChatGPT and Various LLMs", tiny_font, white, screen, width // 2, height - 20)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
LIGHTGREEN = (144, 236, 144)
GREEN = (175, 255, 170)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (1, 0)

    def move(self):
        head = self.body[-1]
        new_head = (head[0] + self.direction[0]*20, head[1] + self.direction[1]*20)
        self.body.append(new_head)
        self.body.pop(0)

    def grow(self):
        tail = self.body[0]
        new_tail = (tail[0] - self.direction[0]*20, tail[1] - self.direction[1]*20)
        self.body.insert(0, new_tail)

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(WINDOW, BLUE, (segment[0], segment[1], 20, 20))

# Apple class
class Apple:
    def __init__(self):
        self.position = (random.randrange(0, WIDTH, 20), random.randrange(0, HEIGHT, 20))

    def draw(self):
        pygame.draw.circle(WINDOW, RED, (self.position[0] + 10, self.position[1] + 10), 10)

    def respawn(self):
        self.position = (random.randrange(0, WIDTH, 20), random.randrange(0, HEIGHT, 20))
    
# Initialize game objects
snake = Snake()
apple = Apple()
apple_counter = 0
game_started = False

# Font for displaying the counter
font = pygame.font.Font(None, 30)

def draw_checkered_pattern():
    for x in range(0, WIDTH, 40):
        for y in range(0, HEIGHT, 40):
            pygame.draw.rect(WINDOW, LIGHTGREEN, (x, y, 20, 20))
            pygame.draw.rect(WINDOW, LIGHTGREEN, (x + 20, y + 20, 20, 20))

def display_buttons():
    play_button = font.render("Play", True, WHITE)
    play_rect = play_button.get_rect(center=(WIDTH//2, HEIGHT//2))
    WINDOW.blit(play_button, play_rect)

    return play_rect

def endscreen_button():
    play_again_button = font.render("Play", True, WHITE)
    again_rect = play_again_button.get_rect(center=(WIDTH//2, HEIGHT//2))
    pygame.draw.rect(WINDOW, BLACK, again_rect)
    WINDOW.blit(play_again_button, again_rect)

    return again_rect

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
    except FileNotFoundError:
        high_score = 0
    return high_score

# Save high score to file
def save_high_score(high_score):
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

# Main game loop
clock = pygame.time.Clock()
game_over = False
game_started = False
high_score = load_high_score()
play_rect = None
again_rect = None

def main_game_loop():
    global high_score
    clock = pygame.time.Clock()
    game_over = False
    game_started = False
    apple_counter = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if game_started:
            if keys[pygame.K_UP] and snake.direction != (0, 1):
                snake.direction = (0, -1)
            elif keys[pygame.K_DOWN] and snake.direction != (0, -1):
                snake.direction = (0, 1)
            elif keys[pygame.K_LEFT] and snake.direction != (1, 0):
                snake.direction = (-1, 0)
            elif keys[pygame.K_RIGHT] and snake.direction != (-1, 0):
                snake.direction = (1, 0)

            snake.move()

            if snake.body[-1] == apple.position:
                snake.grow()
                apple.respawn()
                apple_counter += 1

            if snake.body[-1][0] < 0 or snake.body[-1][0] >= WIDTH or snake.body[-1][1] < 0 or snake.body[-1][1] >= HEIGHT:
                game_started = False
                game_over = True

                if apple_counter > high_score:
                    high_score = apple_counter
                    save_high_score(high_score)

            for segment in snake.body[:-1]:
                if segment == snake.body[-1]:
                    game_started = False
                    game_over = True

            WINDOW.fill(GREEN)
            draw_checkered_pattern()
            snake.draw()
            apple.draw()

            text = font.render("Apples: " + str(apple_counter), True, BLACK)
            WINDOW.blit(text, (10, 10))

        else:
            play_rect = display_buttons()

            if not game_started and play_rect and play_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                game_started = True

        pygame.display.update()
        clock.tick(12)

    return game_over

def end_game_screen():
    global high_score
    text = font.render("High Score: " + str(high_score), True, BLACK)
    WINDOW.blit(text, (10, 30))
    clock = pygame.time.Clock()
    again_rect = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        again_rect = endscreen_button()

        if again_rect and again_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True

        pygame.display.update()
        clock.tick(12)

while True:
    game_over = main_game_loop()

    if game_over:
        if end_game_screen():
            snake = Snake()
            apple = Apple()
        else:
            break

pygame.quit()
sys.exit()

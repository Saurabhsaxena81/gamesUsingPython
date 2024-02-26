import pygame
import sys
import time
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
AQUA = (0, 255, 255)
BLUE = (0, 0, 255)
YELLOW_GREEN = (154, 205, 50)

# Button class
class Button:
    def __init__(self, rect, color, text, speed_multiplier=None, score_multiplier=None):
        self.rect = rect
        self.color = color
        self.text = text
        self.speed_multiplier = speed_multiplier
        self.score_multiplier = score_multiplier

    def draw(self, surface, font):
        pygame.draw.rect(surface, self.color, self.rect)
        text_render = font.render(self.text, True, BLACK)
        text_rect = text_render.get_rect(center=self.rect.center)
        surface.blit(text_render, text_rect)

# Snake game class
class SnakeGame:
    def __init__(self, screen):
        self.screen = screen
        self.snake_color = (0, 255, 0)  # Green
        self.ball_color = RED
        self.snake_size = 10  # Decreased snake size
        self.snake_length = 20  # Initial snake length
        self.snake_speed = 5  # Speed of the snake
        self.snake = [(100, 100) for _ in range(self.snake_length)]  # Initialize snake
        self.direction = "RIGHT"
        self.ball = self.generate_ball_position()
        self.game_over = False
        self.speed_multiplier = 0.5  # Default speed multiplier
        self.score = 0
        self.frame_count = 0

    def draw_snake(self):
        for i, segment in enumerate(self.snake):
            alpha = (i / len(self.snake)) * 255
            pygame.draw.rect(self.screen, (0, 255, 0, alpha), pygame.Rect(segment[0], segment[1], self.snake_size, self.snake_size))

    def move_snake(self):
        if self.game_over:
            return

        head = list(self.snake[0])

        if self.direction == "RIGHT":
            head[0] += int(self.snake_size * self.speed_multiplier)
        elif self.direction == "LEFT":
            head[0] -= int(self.snake_size * self.speed_multiplier)
        elif self.direction == "UP":
            head[1] -= int(self.snake_size * self.speed_multiplier)
        elif self.direction == "DOWN":
            head[1] += int(self.snake_size * self.speed_multiplier)

        # Check if snake collides with boundaries
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            self.game_over = True
            return

        # Check if snake eats the ball
        if self.check_collision(head, self.ball):
            self.snake_length += 1
            self.ball = self.generate_ball_position()
            if self.score_multiplier is not None:
                self.score += self.score_multiplier
        else:
            self.snake.insert(0, tuple(head))
            self.snake = self.snake[:self.snake_length]  # Adjust the snake length

    def generate_ball_position(self):
        x = random.randrange(0, WIDTH - self.snake_size, self.snake_size)
        y = random.randrange(0, HEIGHT - self.snake_size, self.snake_size)
        return x, y

    def draw_ball(self):
        pygame.draw.circle(self.screen, self.ball_color, (self.ball[0] + self.snake_size // 2, self.ball[1] + self.snake_size // 2), self.snake_size // 2)

    def check_collision(self, head, position):
        return head[0] <= position[0] <= head[0] + self.snake_size and head[1] <= position[1] <= head[1] + self.snake_size

    def reset_game(self):
        self.snake_length = 20
        self.snake = [(100, 100) for _ in range(self.snake_length)]
        self.direction = "RIGHT"
        self.ball = self.generate_ball_position()
        self.game_over = False
        self.score = 0

# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)

    easy_button = Button(pygame.Rect(250, 50, 100, 50), (0, 255, 0), "Easy", speed_multiplier=0.4, score_multiplier=1)
    medium_button = Button(pygame.Rect(250, 150, 100, 50), (255, 255, 0), "Medium", speed_multiplier=0.6, score_multiplier=2)
    hard_button = Button(pygame.Rect(250, 250, 100, 50), (255, 0, 0), "Hard", speed_multiplier=0.9, score_multiplier=3)

    buttons = [easy_button, medium_button, hard_button]

    play_button = Button(pygame.Rect(250, 150, 100, 50), YELLOW_GREEN, "Play")  # Initial position off-screen

    snake_game = SnakeGame(screen)
    restart_button = Button(pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50), AQUA, "Restart")
    exit_button = Button(pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 25, 100, 50), RED, "Exit")
    home_button = Button(pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 100, 100, 50), BLUE, "Home")

    score_display = None

    current_layer = 1  # Start with the first layer

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_layer == 1:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            # Handle button clicks here
                            print(f"Clicked on {button.text}")
                            if button.speed_multiplier is not None:
                                snake_game.speed_multiplier = button.speed_multiplier
                            if button.score_multiplier is not None:
                                snake_game.score_multiplier = button.score_multiplier
                            current_layer = 2  # Switch to the second layer
                elif current_layer == 2 and play_button.rect.collidepoint(event.pos):
                    # Handle play button click
                    print("Clicked on Play")
                    current_layer = 3  # Switch to the third layer (Snake Game)
                    snake_game.reset_game()
                elif current_layer == 3 and snake_game.game_over:
                    if restart_button.rect.collidepoint(event.pos):
                        # Handle restart button click
                        print("Clicked on Restart")
                        snake_game.reset_game()
                    elif exit_button.rect.collidepoint(event.pos):
                        # Handle exit button click
                        print("Clicked on Exit")
                        pygame.quit()
                        sys.exit()
                    elif home_button.rect.collidepoint(event.pos):
                        # Handle home button click
                        print("Clicked on Home")
                        current_layer = 1  # Go back to the first layer

            elif event.type == pygame.KEYDOWN:
                if current_layer == 3:
                    if event.key == pygame.K_UP and snake_game.direction != "DOWN":
                        snake_game.direction = "UP"
                    elif event.key == pygame.K_DOWN and snake_game.direction != "UP":
                        snake_game.direction = "DOWN"
                    elif event.key == pygame.K_LEFT and snake_game.direction != "RIGHT":
                        snake_game.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and snake_game.direction != "LEFT":
                        snake_game.direction = "RIGHT"

        # Clear the screen
        screen.fill(BLACK)

        if current_layer == 1:
            # Draw buttons on the first layer
            for button in buttons:
                button.draw(screen, font)
        elif current_layer == 2:
            # Draw the play button on the center of the screen
            play_button.rect.center = (WIDTH // 2, HEIGHT // 2)
            play_button.draw(screen, font)
        elif current_layer == 3:
            # Draw Snake Game on the third layer
            snake_game.move_snake()
            snake_game.draw_snake()
            snake_game.draw_ball()

            # Check if the game is over
            if snake_game.game_over:
                restart_button.rect.center = (WIDTH // 2, HEIGHT // 2 - 25)
                exit_button.rect.center = (WIDTH // 2, HEIGHT // 2 + 25)
                home_button.rect.center = (WIDTH // 2, HEIGHT // 2 - 75)
                restart_button.draw(screen, font)
                exit_button.draw(screen, font)
                home_button.draw(screen, font)

                # Display score
                score_text = f"Score: {snake_game.score}"
                score_render = font.render(score_text, True, ORANGE)
                score_rect = score_render.get_rect(topleft=(10, 10))
                screen.blit(score_render, score_rect)
        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()


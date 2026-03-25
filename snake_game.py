import pygame
import random
import sys

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (200, 0, 0)
GRAY = (40, 40, 40)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_dir):
        # Prevent reversing directly
        opposite = (-new_dir[0], -new_dir[1])
        if opposite != self.direction:
            self.direction = new_dir

    def eat(self):
        self.grow = True

    def check_wall_collision(self):
        x, y = self.body[0]
        return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT

    def check_self_collision(self):
        return self.body[0] in self.body[1:]

    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            color = GREEN if i == 0 else DARK_GREEN
            rect = pygame.Rect(x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2)
            pygame.draw.rect(surface, color, rect, border_radius=4)


class Food:
    def __init__(self, snake_body):
        self.position = self.spawn(snake_body)

    def spawn(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                return pos

    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * CELL_SIZE + 2, y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
        pygame.draw.rect(surface, RED, rect, border_radius=6)


def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WINDOW_WIDTH, y))


def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont("monospace", size, bold=True)
    label = font.render(text, True, color)
    rect = label.get_rect(center=(x, y))
    surface.blit(label, rect)


def show_screen(surface, title, subtitle):
    surface.fill(BLACK)
    draw_text(surface, title, 48, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40)
    draw_text(surface, subtitle, 22, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    show_screen(screen, "SNAKE", "Press ENTER to start")

    while True:
        snake = Snake()
        food = Food(snake.body)
        score = 0
        running = True

        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        snake.change_direction(UP)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        snake.change_direction(DOWN)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        snake.change_direction(LEFT)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        snake.change_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            snake.move()

            if snake.check_wall_collision() or snake.check_self_collision():
                running = False
                break

            if snake.body[0] == food.position:
                snake.eat()
                score += 1
                food = Food(snake.body)

            # Draw
            screen.fill(BLACK)
            draw_grid(screen)
            snake.draw(screen)
            food.draw(screen)
            draw_text(screen, f"Score: {score}", 24, WINDOW_WIDTH // 2, 14)
            pygame.display.flip()

        show_screen(screen, f"Game Over! Score: {score}", "Press ENTER to play again")


if __name__ == "__main__":
    main()

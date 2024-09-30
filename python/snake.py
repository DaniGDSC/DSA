import random
import pygame

class SnakeGame:
    def __init__(self, width=20, height=20, cell_size=20):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.reset()

    def reset(self):
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = (1, 0)  # Right direction by default
        self.food = None
        self.score = 0
        self.generate_food()

    def move_snake(self):
        head_x, head_y = self.snake[0]
        new_head_x, new_head_y = head_x + self.direction[0], head_y + self.direction[1]
        if not (0 <= new_head_x < self.width and 0 <= new_head_y < self.height):
            raise GameOverException("Snake went out of bounds")

        for x, y in self.snake:
            if new_head_x == x and new_head_y == y:
                raise GameOverException("Snake ran into itself")
        
        self.snake.insert(0, (new_head_x, new_head_y))
        if self.food is not None and new_head_x == self.food[0] and new_head_y == self.food[1]:
            self.score += 1
            self.generate_food()
        else:
            self.snake.pop()

    def generate_food(self):
        while True:
            food_x, food_y = random.randrange(self.width), random.randrange(self.height)
            if (food_x, food_y) not in self.snake:
                self.food = (food_x, food_y)
                break

    def change_direction(self, direction):
        if direction == "left" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif direction == "right" and self.direction != (-1, 0):
            self.direction = (1, 0)
        elif direction == "up" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif direction == "down" and self.direction != (0, -1):
            self.direction = (0, 1)

class GameOverException(Exception):
    pass

def main():
    pygame.init()
    width, height = 20, 20
    cell_size = 20
    screen_width, screen_height = width * cell_size, height * cell_size
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake Game")

    game = SnakeGame(width, height, cell_size)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.change_direction("left")
                elif event.key == pygame.K_RIGHT:
                    game.change_direction("right")
                elif event.key == pygame.K_UP:
                    game.change_direction("up")
                elif event.key == pygame.K_DOWN:
                    game.change_direction("down")
                elif event.key == pygame.K_r:
                    game.reset()

        try:
            game.move_snake()
        except GameOverException as e:
            print(f"Game Over: {e}")
            text = font.render(f"Game Over! Score: {game.score}. Press R to restart", True, (255, 0, 0))
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
            pygame.display.flip()
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        game.reset()
                        waiting_for_restart = False
            continue

        screen.fill((0, 0, 0))  # Black background

        # Draw snake
        for segment in game.snake:
            pygame.draw.rect(screen, (0, 255, 0), (segment[0] * cell_size, segment[1] * cell_size, cell_size, cell_size))

        # Draw food
        if game.food:
            pygame.draw.rect(screen, (255, 0, 0), (game.food[0] * cell_size, game.food[1] * cell_size, cell_size, cell_size))

        # Draw score
        score_text = font.render(f"Score: {game.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(10)  # Control game speed

if __name__ == "__main__":
    main()
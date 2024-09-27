from random import randint
import pygame
import random

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
WHITE = (255, 255, 255)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Настройка игрового окна:
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()
SPEED = 10


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=None, body_color=WHITE):
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Метод для отрисовки объекта на экране."""
        raise NotImplementedError('Только в дочерних')


class Apple(GameObject):
    """Класс для яблока, которое может быть съедено змейкой."""

    def __init__(
        self,
        position=None,
        body_color=APPLE_COLOR,
        occupied_cells=[]
    ):
        super().__init__(position=position, body_color=body_color)
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells=[]):
        """Определяет новую позицию яблока, избегая занятых ячеек."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            if self.position not in occupied_cells:
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки, которая движется по игровому полю."""

    def __init__(self, position=CENTER_POSITION, body_color=SNAKE_COLOR):
        super().__init__(position, body_color=body_color)
        self.reset()
        self.direction = (1, 0)

    def reset(self):
        """Сбрасывает состояние змейки."""
        self.positions = [self.position]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.last = None
        self.next_direction = self.direction

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def grow(self):
        """Увеличивает длину змейки."""
        if self.last:
            self.positions.append(self.last)
            self.last = None

    def move(self):
        """Перемещает змейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        self.last = (head_x, head_y)

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)
        self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        head_x, head_y = self.get_head_position()
        rect = pygame.Rect((head_x, head_y), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last is not None:
            rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

    def update_direction(self):
        """Обновляет направление змейки на основе следующего направления."""
        self.direction = self.next_direction


def handle_keys(game_object):
    """Управление"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверяем, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовываем все объекты

        apple.draw()
        snake.draw()

        pygame.display.flip()
        clock.tick(SPEED)

    pygame.quit()


if __name__ == "__main__":
    main()


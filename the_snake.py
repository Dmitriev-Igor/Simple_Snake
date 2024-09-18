from random import randint
import pygame

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

    def __init__(self, occupied_cells=None):
        super().__init__(body_color=APPLE_COLOR)
        self.occupied_cells = occupied_cells or []
        self.randomize_position()

    def randomize_position(self):
        """Определяет новую позицию яблока, избегая занятых ячеек."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (x, y)
            if new_position not in self.occupied_cells:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки, которая движется по игровому полю."""

    def __init__(self, position=CENTER_POSITION):
        super().__init__(position, body_color=SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Сбрасывает состояние змейки."""
        self.positions = [self.position]
        self.direction = self.next_direction = RIGHT

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def grow(self):
        """Увеличивает длину змейки."""
        self.positions.append(self.positions[-1])

    def move(self, grow=False):
        """Перемещает змейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)
        if not grow:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def update_direction(self):
        """Обновляет направление движения змейки на следующее направление."""
        if (self.next_direction[0] * -1, self.next_direction[1] * -1) != self.direction:
            self.direction = self.next_direction


def handle_keys(event, snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    if event.key == pygame.K_UP:
        snake.next_direction = UP
    elif event.key == pygame.K_DOWN:
        snake.next_direction = DOWN
    elif event.key == pygame.K_LEFT:
        snake.next_direction = LEFT
    elif event.key == pygame.K_RIGHT:
        snake.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    # Создаем объекты змейки и яблока
    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)

    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                handle_keys(event, snake)

        # Обновляем направление змейки
        snake.update_direction()
        # Перемещаем змейку
        snake.move()

        # Проверяем, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.grow()  # Увеличиваем змейку
            apple.randomize_position()  # Позиция яблока обновляется

        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()

        # Обновить занятые клетки яблока
        apple.occupied_cells = snake.positions

        # Отрисовываем все объекты
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.flip()
        clock.tick(SPEED)

    pygame.quit()


if __name__ == "__main__":
    main()

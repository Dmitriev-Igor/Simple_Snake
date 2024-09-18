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


# Тут опишите все классы игры.
...


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

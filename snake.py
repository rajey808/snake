import pygame
from pygame import freetype
import random
import sys

# initialise Pygame
pygame.init()
clock_speed = 5

# setup the window
window_width = 720
window_height = 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake Game')
font = pygame.font.Font('freesansbold.ttf', 32)



# setup game board
cell_size = 20
game_board_width = window_width // cell_size
game_board_height = window_height // cell_size
game_board = [[0] * game_board_width for x in range(game_board_height)]

snake_colour = (255,255,255)
food_colour = (255,0,0)

def create__initial_snake():
    # setup initial snake
    snake = [(game_board_width // 2, game_board_height // 2),
            (game_board_width // 2, game_board_height // 2 + 1),
            (game_board_width // 2, game_board_height // 2 + 2)]
    return snake

def draw_snake(snake):
    # draw snake 
    for segment in snake:
        x, y = segment
        game_board[segment[1]][segment[0]] = 1
        rectangle = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
        pygame.draw.rect(window, snake_colour, rectangle)

def update_snake(snake, dx, dy, food_eaten):
    new_snake = []

    # add new segment to snake at head
    head = snake[0]
    game_board[head[1] + dy][head[0] + dx] = 1
    new_snake.append((head[0] + dx, head[1] + dy))

    # update last segment to non snake if food not eaten this round
    if not food_eaten:
        tail = snake[-1]
        x,y = tail
        game_board[tail[1]][tail[0]] = 0
        rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
        pygame.draw.rect(window, (0,0,0), rect)

    # change each snake segment by dx, dy
    for i in range(1, len(snake)):
        prev_segment = snake[i-1]
        x,y = prev_segment
        game_board[prev_segment[1]][prev_segment[0]] = 1
        new_snake.append((x,y))

    if food_eaten:
        tail = snake[-1]
        x,y = tail
        game_board[tail[1]][tail[0]] = 1
        new_snake.append((x,y))

    return new_snake

def create_food():
    # setup food    
    ran_x = random.randint(0, game_board_width - 1)
    ran_y = random.randint(0, game_board_height - 1)
    
    while game_board[ran_y][ran_x] == 1:
        ran_x = random.randint(0, game_board_width - 1)
        ran_y = random.randint(0, game_board_height - 1)

    food = (ran_x, ran_y)
    game_board[food[1]][food[0]] = 2
    return food

def draw_food(food):
    x,y = food
    rectangle = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
    pygame.draw.rect(window, food_colour, rectangle)

def check_obstacle(snake):
    game_over = False

    snake_head = snake[0]
    x,y = snake_head

    if 0 > x  or x > game_board_width or 0 > y  or y > game_board_width:
        game_over = True

    for segment in snake[1:]:
        if segment == snake_head:
            game_over = True

    return game_over

def main():

    snake = create__initial_snake()
    draw_snake(snake)
    food = create_food()
    draw_food(food)

    # set up the clock
    clock = pygame.time.Clock()
    direction = "UP"

    game_over = False
    score = 0
    while not game_over:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    # move the snake left
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    # move the snake right
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    # move the snake up
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    # move the snake down
                    direction = "DOWN"

        snake_head = snake[0]
        dx, dy = 0, 0
        if direction == "UP":
            dx, dy = 0, -1
        elif direction == "DOWN":
            dx, dy = 0, 1
        elif direction == "LEFT":
            dx, dy = -1, 0
        elif direction == "RIGHT":
            dx, dy = 1, 0

        food_eaten = False

        if food == snake_head:
            food_eaten = True
            score += 1

        snake = update_snake(snake, dx, dy, food_eaten)

        if food_eaten:
            food = create_food()

        # todo : add new food when snake eats food, i.e. snake head position = food position
        # but need to add in the next loop iteration 

        game_over = check_obstacle(snake)

        # draw the game board every loop
        for y in range(game_board_height):
            for x in range(game_board_width):
                # draw snake
                if game_board[y][x] == 1 :
                    draw_snake(snake)
                    #rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                    #pygame.draw.rect(window, snake_colour, rect)
                elif game_board[y][x]  == 2 :
                    draw_food(food)
                    #rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size) 
                    #pygame.draw.rect(window, food_colour, rect)

        if not game_over:

            # update display
            pygame.display.update()

            # set the game speed
            clock.tick(clock_speed)
            
        else:
            text = font.render('GAME OVER', True, (255,255,255), (0,0,0))
            textRect = text.get_rect()
            textRect.center = (window_width// 2, window_height // 2)
            window.blit(text, textRect)

            text = font.render(f'Score: {score}', True, (255,255,255), (0,0,0))
            textRect = text.get_rect()
            textRect.center = (window_width// 2, window_height // 2 + 50)
            window.blit(text, textRect)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
    
if __name__ == "__main__":
    main()
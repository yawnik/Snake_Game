from machine import Pin, I2C
from time import sleep_ms
import ssd1306
import random

# initialize display
i2c = I2C(-1, scl=Pin(9), sda=Pin(8))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# initialize buttons
btn_top = Pin(5, Pin.IN, Pin.PULL_UP)
btn_bottom = Pin(7, Pin.IN, Pin.PULL_UP)

# initialize ball position and velocity
ball_x = 64
ball_y = 32
ball_vx = 1
ball_vy = 1
BALL_SIZE = 4
BALL_SPEED = 3
global ball_speed_x, ball_speed_y
ball_speed_x = BALL_SPEED
ball_speed_y = BALL_SPEED

# initialize paddle position
paddle_y = 27
PADDLE_WIDTH = 2
PADDLE_HEIGHT = 20

# initialize score
score = 0

screen_width = 128
screen_height = 64

ball_start_x = screen_width // 2
ball_start_y = screen_height // 2

# define function to draw paddle
def draw_paddle():
    display.fill_rect(0, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, 1)

# define function to update paddle position
def update_paddle_position():
    global paddle_y
    if not btn_top.value():
        paddle_y = max(0, paddle_y - 2)
    if not btn_bottom.value():
        paddle_y = min(screen_height - PADDLE_HEIGHT, paddle_y + 2)

# define function to draw ball
def draw_ball():
    display.fill_rect(int(ball_x - BALL_SIZE/2), int(ball_y - BALL_SIZE/2), BALL_SIZE, BALL_SIZE, 1)

# define function to update ball position
def update_ball_position():
    global score, ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check if ball hits top or bottom wall
    if ball_y < BALL_SIZE/2 or ball_y > screen_height - BALL_SIZE/2:
        ball_speed_y *= -1

    # Check if ball hits left or right wall
    if ball_x < BALL_SIZE/2:
        ball_speed_x *= -1

    # Check if ball hits paddle
    if ball_x > screen_width - BALL_SIZE - PADDLE_WIDTH and paddle_y - BALL_SIZE/2 < ball_y < paddle_y + PADDLE_HEIGHT + BALL_SIZE/2:
        ball_speed_x *= -1
        score += 1

    # Check if game over
    if ball_x > screen_width - BALL_SIZE:
        game_over = True

# define function to draw score
def draw_score():
    display.fill_rect(0, 0, 30, 10, 0)
    display.text("Score: " + str(score), 0, 0, 1)

# define function to reset ball
def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = ball_start_x
    ball_y = ball_start_y
    ball_speed_x = BALL_SPEED * random.choice([-1, 1])
    ball_speed_y = BALL_SPEED * random.choice([-1, 1])

def restart_game():
    global score, ball_speed_x, ball_speed_y
    score = 0
    ball_speed_x = BALL_SPEED * random.choice([-1, 1])
    ball_speed_y = BALL_SPEED * random.choice([-1, 1])
    reset_ball()

# define game loop
def run_game():
    global game_over
    
    # reset game variables
    game_over = False
    global score
    score = 0
    reset_ball()
    
    while not game_over:
        # clear display
        display.fill(0)
        
        # update paddle position
        update_paddle_position()
        
        # update ball position
        update_ball_position()
        
        # draw objects
        draw_paddle()
        draw_ball()
        draw_score()
        display.show()
        
        # delay to control game speed
        sleep_ms(10)
        
        # check if game over
        if game_over:
            display.fill(0)
            display.text("Game over!", 30, 20, 1)
            display.text("Score: " + str(score), 30, 40, 1)
            display.show()
            sleep_ms(2000)
            
    # restart game after game over
    restart_game()
    
# start game loop
while True:
    run_game()


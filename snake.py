import machine
import ssd1306
import time
import random
import sys

# Define pins for buttons and display
button_up = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
button_down = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP)
button_left = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
button_right = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)
scl_pin = machine.Pin(9, machine.Pin.OUT)
sda_pin = machine.Pin(8, machine.Pin.OUT)

# Initialize display and clear it
i2c = machine.I2C(-1, scl=scl_pin, sda=sda_pin)
display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.fill(0)
display.show()

#Bootscreen
display.fill(0)
display.text("Yantendo", 30, 0)
display.text("Matchboy", 30, 10)
display.text("Snake Minispiel", 4, 20)
display.text("Yannik Helms", 12, 40)
display.text("ETS2022", 34, 50)
display.show()
time.sleep(1.5)

# Define starting positions for the snake and the food
snake = [(28, 28), (24, 28), (20, 28)]
food = (random.randint(0, 118)//4*4, random.randint(0, 58)//4*4)

#############################

# Definieren Sie die Konstanten für das Spielfeld
FIELD_WIDTH = 124
FIELD_HEIGHT = 60
FIELD_X = 1
FIELD_Y = 1

# Definieren Sie die Funktion, um den Rahmen um das Spielfeld zu zeichnen
def draw_field_border():
    display.rect(FIELD_X-1, FIELD_Y-1, FIELD_WIDTH+2, FIELD_HEIGHT+2, 1)
    
#####################################

# Define functions for drawing the snake and the food
def draw_snake():
    for segment in snake:
        display.rect(segment[0], segment[1], 5, 5, 1)

def draw_food():
    display.rect(food[0], food[1], 5, 5, 1)

# Define function for drawing the game over message
def draw_game_over():
    display.fill(0)
    display.text("GAME OVER :(", 16, 0)
    display.text("Score: {}".format(len(snake)), 28, 20)
    display.text("Zum neu starten", 6, 40)
    display.text("Taste druecken", 8, 50)
    display.show()

# Spawn a new food
def spawn_food():
    while True:
        # Generate random coordinates for the food
        x = random.randrange(0, 124, 4)
        y = random.randrange(0, 60, 4)

        # Check if the food is not on the snake's body
        if (x, y) not in snake:
            # Return the food's coordinates
            return (x, y)


# Define variables for the snake's direction
dx = 4
dy = 0

# Define a variable for the game's state
game_over = False

# Define a function for detecting button presses
def button_pressed(pin):
    time.sleep(0.02)
    return not pin.value()

# Define a function to start a new game
def new_game():
    global dx, dy, game_over, snake, food
    
    # Reset variables
    dx = 2
    dy = 0
    game_over = False
    snake = [(32, 32), (30, 32), (28, 32)]
    
    # Generate the initial food position
    food = (random.randint(0, 63)*2, random.randint(0, 31)*2)
    
    # Clear the display
    display.fill(0)
    display.show()
    
# Reset the game
def reset_game():
    global snake, food, direction, game_over, score

    # Initialize the snake
    snake = [(64, 16), (64, 18), (64, 20)]

    # Initialize the food
    food = spawn_food()

    # Initialize the direction
    direction = "UP"

    # Initialize the game over flag
    game_over = False

    # Initialize the score
    score = 0

    # Clear the display
    display.fill(0)


# Display the start message
display.fill(0)
display.text("Zum starten", 20, 20)
display.text("beliebige Taste", 6, 30)
display.text("druecken!", 25, 40)
display.show()

# Wait for a button press to start the game
while not any([button_pressed(button_up), button_pressed(button_down), button_pressed(button_left), button_pressed(button_right)]):
    pass

# Start the game
new_game()
# Zeichnen des Rahmens

display.rect(0, 0, 128, 64, 1)

# Game loop
while True:
    # Check for button presses and update the snake's direction
    if button_pressed(button_up) and dy == 0:
        dx = 0
        dy = -2
    elif button_pressed(button_down) and dy == 0:
        dx = 0
        dy = 2
    elif button_pressed(button_left) and dx == 0:
        dx = -2
        dy = 0
    elif button_pressed(button_right) and dx == 0:
        dx = 2
        dy = 0
        
    # Update the position of the snake's head
    head = snake[0]
    new_head = (head[0] + dx, head[1] + dy)
    
    # Check for collision with walls
    if new_head[0] < 0 or new_head[0] > 126 or new_head[1] < 0 or new_head[1] > 62:
        game_over = True
    
    # Check for collision with snake's body
    if new_head in snake:
        game_over = True
    
    # Check for collision with food
    if new_head[0] == food[0] and new_head[1] == food[1]:
        # Add new segment to the snake
        snake.insert(0, new_head)
        
        # Generate new food position
        while True:
            food = (random.randint(0, 63)*2, random.randint(0, 31)*2)
            if food not in snake:
                break
    else:
        # Move the snake
        snake.insert(0, new_head)
        snake.pop()
    
    # Clear the display
    display.fill(0)
    
    # Draw the snake and the food
    draw_snake()
    draw_food()
    display.show()
    
# Check if the game is over
    if game_over:
        # Draw the game over message
        draw_game_over()

        # Wait for a button press to start a new game
        while True:
            # Check for button presses
            if button_up.value() == 0 or button_left.value() == 0 or button_right.value() == 0 or button_down.value() == 0:
                # Reset the game and start a new one
                reset_game()
                break
#             elif button_down.value() == 0:
#                 # Turn off the display and exit the game
#                 display.poweroff()
#                 sys.exit()
            else: #button_left.value() == 0 or button_right.value() == 0:
                # Do nothing - wait for an actual direction button press
                pass



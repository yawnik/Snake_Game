# Flappy Bird

import machine
import ssd1306
import time
import urandom

from machine import Pin, I2C

i2c = I2C(scl=Pin(9), sda=Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

button_up = Pin(5, Pin.IN, Pin.PULL_UP)
button_down = Pin(7, Pin.IN, Pin.PULL_UP)
button_left = Pin(21, Pin.IN, Pin.PULL_UP)
button_right = Pin(6, Pin.IN, Pin.PULL_UP)

player_y = 32
player_v = 0
player_size = 6

pipe_gap = 24
pipe_width = 8
pipe_spacing = 25
pipe_speed = 2

pipe_x = 128
pipe_y = urandom.getrandbits(5) * 2 + 16

score = 0

def draw_player():
    oled.fill_rect(4, player_y - player_size // 2, player_size, player_size, 1)

def draw_pipe():
    oled.fill_rect(pipe_x, 0, pipe_width, pipe_y - pipe_gap // 2, 1)
    oled.fill_rect(pipe_x, pipe_y + pipe_gap // 2, pipe_width, 64 - pipe_y - pipe_gap // 2, 1)

def draw_score():
    oled.text(str(score), 64, 0, 1)
    oled.hline(0, 9, 128, 1)

def update_player():
    global player_y, player_v
    player_v += 1
    player_y += player_v
    if player_y + player_size // 2 >= 64:
        player_y = 64 - player_size // 2
        player_v = 0
    if player_y - player_size // 2 <= 10:
        player_y = 10 + player_size // 2
        player_v = 0

def update_pipe():
    global pipe_x, pipe_y, score
    pipe_x -= pipe_speed
    if pipe_x + pipe_width < 0:
        pipe_x = 128
        pipe_y = urandom.getrandbits(5) * 2 + 16
        score += 1

def check_collision():
    if pipe_x < player_size + 4 < pipe_x + pipe_width and (player_y + player_size // 2 > pipe_y + pipe_gap // 2 or player_y - player_size // 2 < pipe_y - pipe_gap // 2):
        return True
    else:
        return False

def start_game():
    global player_y, player_v, score, pipe_x, pipe_y
    player_y = 32
    player_v = 0
    score = 0
    pipe_x = 128
    pipe_y = urandom.getrandbits(5) * 2 + 16

    oled.fill(0)
    oled.text("Flappy Bird", 20, 20, 1)
    oled.show()
    time.sleep(2)

while True:
    oled.fill(0)
    draw_player()
    draw_pipe()
    draw_score()
    oled.show()

    update_player()
    update_pipe()

    if check_collision():
        oled.fill(0)
        oled.text("Game Over", 25, 20, 1)
        oled.text("Score: " + str(score), 25, 40, 1)
        oled.show()
        time.sleep(2)
        start_game()

    if not button_up.value():
        player_v = -4

    if not button_down.value():
        player_v = 4

    if not button_left.value():
        pipe_speed = 1

    if not button_right.value():
        pipe_speed = 2

    time.sleep(0.02)

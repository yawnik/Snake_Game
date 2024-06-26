from machine import Pin, I2C, ADC, PWM, freq
from framebuf import FrameBuffer, MONO_VLSB
from ssd1306 import SSD1306_I2C
import utime, urandom, gc
import machine

SCL_PIN = 9
SDA_PIN = 8
# JOYSTICK_X_PIN = 34
# JOYSTICK_Y_PIN = 33
# JOYSTICK_SW_PIN = 5
# BUZZER_PIN = 23
# LED_R_PIN = 17
# LED_G_PIN = 16
# LED_B_PIN = 21
# RAND_SEED_PIN = 35

SCREEN_W = 128
SCREEN_H = 64
DELAY = 10

BRICK_W = 16
BRICK_H = 8
BRICK_ROW = 4
brick_buf = FrameBuffer(bytearray(
    [0x00, 0x7e, 0x7e, 0x7e,
     0x7e, 0x7e, 0x7e, 0x7e,
     0x7e, 0x7e, 0x7e, 0x7e,
     0x7e, 0x7e, 0x7e, 0x00]
    ), BRICK_W, BRICK_H, MONO_VLSB)

PADDLE_W = 16
PADDLE_H = 4
PADDLE_SPEED = 8
paddle_buf = FrameBuffer(bytearray(
    [0x03, 0x07, 0x07, 0x07,
     0x07, 0x07, 0x07, 0x07,
     0x07, 0x07, 0x07, 0x07,
     0x07, 0x07, 0x07, 0x03]
    ), PADDLE_W, PADDLE_H, MONO_VLSB)

BALL_W = 4
BALL_H = 4
BALL_MIN_SPEED = 2
ball_buf = FrameBuffer(bytearray(
    [0x06, 0x0f, 0x0f, 0x06]
    ), BALL_W, BALL_H, MONO_VLSB)

# adc_x = ADC(Pin(JOYSTICK_X_PIN))
# adc_x.atten(ADC.ATTN_11DB)
# adc_y = ADC(Pin(JOYSTICK_Y_PIN))
# adc_y.atten(ADC.ATTN_11DB)
# sw = Pin(JOYSTICK_SW_PIN, Pin.IN, Pin.PULL_UP)
sw = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
swr = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)
swl = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
display = SSD1306_I2C(SCREEN_W, SCREEN_H,
                      I2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN)))

#rand_seed = ADC(Pin(RAND_SEED_PIN))
# seed = 0
# for _ in range(1000):
#     seed += rand_seed.read()
# seed *= 10
# urandom.seed(seed * 10)
# 
# gc.enable()


class Sprite:
    
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Brick(Sprite):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.exist = True
    
    def hide(self):
        self.exist = False


class Paddle(Sprite):
    
    def setSpeed(self, speed_x):
        self.speed_x = speed_x
    
    def move(self, direction):
        if direction == 'left':
            self.speed_x = abs(self.speed_x) * -1
        elif direction == 'right':
            self.speed_x = abs(self.speed_x)
        self.x += self.speed_x
        if self.x < 0:
            self.x = 0
        if self.x + self.w >= SCREEN_W:
            self.x = SCREEN_W - self.w - 1
            
# Define a function for detecting button presses
def button_pressed(pin):
    utime.sleep(0.02)
    return not pin.value()

class Ball(Sprite):
    
    def setSpeed(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y
    
    def randomChangeSpeed(self):
        speed_x_sign = -1 if self.speed_x < 0 else 1
        speed_y_sign = -1 if self.speed_y < 0 else 1
        self.speed_x = (urandom.getrandbits(1) + BALL_MIN_SPEED) * speed_x_sign
        self.speed_y = (urandom.getrandbits(1) + BALL_MIN_SPEED) * speed_y_sign
    
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x < 0:
            self.x = 0
        if self.x + self.w >= SCREEN_W:
            self.x = SCREEN_W - self.w - 1
        if self.y < 0:
            self.y = 0
        if self.y + self.h >= SCREEN_H:
            self.y = SCREEN_H - self.h - 1
    
#     def setBuzzerPin(self, buzzer_pin):
#         self.buzzer_pin = buzzer_pin
    
#     def buzzerBeep(self, note, delay):
#         buzzer = PWM(Pin(self.buzzer_pin), freq=note, duty=512)
#         utime.sleep_ms(delay)
#         buzzer.deinit()
    
    def isCollidedWith(self, other):
        return (other.x - self.w) < self.x < (other.x + other.w) and (other.y - self.h) < self.y < (other.y + other.h)

    def bounceFromBrick(self, brick):
        self_center_x = self.x + self.w // 2
        self_center_y = self.y + self.h // 2
        brick_center_x = brick.x + brick.w // 2
        brick_center_y = brick.y + brick.h // 2
        x_diff = brick_center_x - self_center_x
        y_diff = brick_center_y - self_center_y
        if (brick.x <= self_center_x <= brick.x + brick.w):
            #self.buzzerBeep(233, 25)
            if y_diff <= 0:
                self.speed_y = abs(self.speed_y)
            else:
                self.speed_y = abs(self.speed_y) * -1
        elif (brick.y <= self_center_y <= brick.y + brick.h):
            #self.buzzerBeep(233, 25)
            if x_diff <= 0:
                self.speed_x = abs(self.speed_x)
            else:
                self.speed_x = abs(self.speed_x) * -1
        self.randomChangeSpeed()
            
    def bounceFromPaddleIfNeeded(self, paddle):
        if self.isCollidedWith(paddle):
            #self.buzzerBeep(932, 10)
            self.speed_y = abs(self.speed_y) * -1
            self.randomChangeSpeed()
            if urandom.getrandbits(2) == 0:
                self.speed_x *= -1
            
    def bounceFromWallIfNeeded(self):
        if self.speed_x < 0 and self.x <= 0:
            #self.buzzerBeep(466, 15)
            self.speed_x = abs(self.speed_x)
        elif self.speed_x > 0 and self.x + self.w >= SCREEN_W - 1:
            #self.buzzerBeep(466, 15)
            self.speed_x = abs(self.speed_x) * -1
        if self.speed_y < 0 and self.y <= 0:
            #self.buzzerBeep(440, 15)
            self.speed_y = abs(self.speed_y)

    def isFailedToBeCatchedBy(self, paddle):
        return not self.isCollidedWith(paddle) and (self.y + self.h) >= SCREEN_H - 1


score = 0
score_show = True
bricks = []
paddle = None
ball = None

def resetArcade():
    global bricks
    global paddle
    global ball
    global score
    global score_show
    score = 0
    score_show = True
    bricks.clear()
    for x in range(0, SCREEN_W, BRICK_W):
        for y in range(0, BRICK_H * BRICK_ROW, BRICK_H):
            bricks.append(Brick(x, y, BRICK_W, BRICK_H))
    paddle = Paddle((SCREEN_W - PADDLE_W) // 2,
                     SCREEN_H - PADDLE_H - 1,
                     PADDLE_W, PADDLE_H)
    paddle.setSpeed(PADDLE_SPEED)
    ball = Ball((SCREEN_W - BALL_W) // 2,
                 SCREEN_H - PADDLE_H - BALL_H - 1,
                 BALL_W, BALL_H)
    ball.setSpeed(BALL_MIN_SPEED, BALL_MIN_SPEED * -1)
    ball.randomChangeSpeed()
    #ball.setBuzzerPin(BUZZER_PIN)

def refreshScreen():
    display.fill(0)
    for brick in bricks:
        if brick.exist:
            display.blit(brick_buf, brick.x, brick.y)
    display.blit(ball_buf, ball.x, ball.y)
    display.blit(paddle_buf, paddle.x, paddle.y)
    global score_show
    if score_show:
        score_x = 0
        if paddle.x + paddle.w // 2 <= SCREEN_W // 2:
            score_x = SCREEN_W - PADDLE_W - 1
        display.text('{:02d}'.format(score), score_x, SCREEN_H - 8 - 1, 1)
    score_show = not score_show
    display.show()

def displayClear():
    display.fill(0)
    display.show()

def displayCenterText(text):
    display.fill(0)
    display.text(text, (SCREEN_W - len(text) * 8) // 2, SCREEN_H // 2)
    display.show()

def displayCenterTextOneByOne(text, delay):
    display.fill(0)
    for i in range(1, len(text) + 1):
        displayCenterText(text[:i] + ' ' * (len(text) - i))
        utime.sleep_ms(delay)
    display.show()

# def setLED(r, g, b):
#     led_r = PWM(Pin(LED_R_PIN), freq=1000, duty=r)
#     led_g = PWM(Pin(LED_G_PIN), freq=1000, duty=g)
#     led_b = PWM(Pin(LED_B_PIN), freq=1000, duty=b)

# def buzzerSing(notes, tempo_ms):
#     for note, delay in notes:
#         buzzer = PWM(Pin(BUZZER_PIN), freq=note, duty=512)
#         utime.sleep_ms(int(delay * tempo_ms))
#         buzzer.deinit()


#analog_input_center = adc_x.read() // 4
# score_show = False
# gc.collect()
# 
# setLED(256, 256, 32)
# utime.sleep(0.1)
# displayCenterText('Py-Breakout')
# notes = (
#     (392, 1),
#     (523, 1),
#     (659, 1),
#     (784, 2),
#     (659, 1),
#     (784, 4),
#     )
# buzzerSing(notes, 125)
# utime.sleep(1)


while True:
    
    while True:
        if score_show:
            displayCenterText('PRESS TO START')
        else:
            displayClear()
        score_show = not score_show
        for _ in range(10):
            if sw.value() == 0:
                break
            utime.sleep_ms(50)
        else:
            continue
        break

    #setLED(512, 512, 64)
    notes = (
        (523, 1),
        (587, 1),
        (659, 1),
        (698, 1),
        (784, 1),
        )
    #buzzerSing(notes, 50)
    displayCenterTextOneByOne('Ready', 100)
    utime.sleep(0.5)
    resetArcade()

    while True:
    
#         analog_input = adc_x.read() // 4
#         if analog_input <= analog_input_center - 200:
#             paddle.move('left')
#         elif analog_input >= analog_input_center + 200:
#             paddle.move('right')
        if button_pressed(swl):
            paddle.move('left')
        elif button_pressed(swr):
            paddle.move('right')

    
        for brick in reversed(bricks):
            if brick.exist and ball.isCollidedWith(brick):
                #setLED(128, 1023, 1023)
                brick.hide()
                score += 1
                ball.bounceFromBrick(brick)
                #setLED(512, 512, 64)
                break
        
        ball.move()
        ball.bounceFromWallIfNeeded()
        ball.bounceFromPaddleIfNeeded(paddle)
        refreshScreen()

        if score == len(bricks):
            cleared = True
            break

        if ball.isFailedToBeCatchedBy(paddle):
            cleared = False
            break
    
        gc.collect()
        utime.sleep_ms(DELAY)


    displayClear()
    refreshScreen()
    utime.sleep(0.1)
    score_show = True
    refreshScreen()
    
    if cleared:
        setLED(128, 1023, 0)
        notes = (
            (494, 1),
            (659, 3),
            (494, 1),
            (659, 3),
            (494, 1),
            (659, 5),
            )
        buzzerSing(notes, 100)
        utime.sleep(1)
        displayCenterTextOneByOne('GAME CLEARED', 100)
    else:
        #setLED(1023, 128, 0)
        notes = (
            (784, 1),
            (659, 1),
            (523, 1),
            (392, 2),
            (494, 1),
            (523, 4),
            )
        #buzzerSing(notes, 125)
        utime.sleep(1)
        displayCenterTextOneByOne('GAME OVER', 200)
        
    utime.sleep(1)
    displayClear()
    #setLED(128, 128, 16)
    utime.sleep(0.1)
    displayCenterText('SCORE: ' + str(score))
    utime.sleep(1.5)
    #setLED(256, 256, 16)
    displayClear()
    score_show = False

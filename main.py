from machine import Pin, I2C
import ssd1306
import time

# Initialisierung des OLED-Displays
i2c = I2C(-1, scl=Pin(9), sda=Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Anzeigen der Spielauswahl auf dem OLED-Display
def show_menu():
    oled.fill(0)
    oled.text('Waehle ein Spiel:', 0, 0)
    oled.text('UP. Snake', 0, 20)
    oled.text('DN. Breakout', 0, 30)
    oled.text('LT. Flappy', 0, 40)
    oled.text('RT. coming soon', 0, 50)
    oled.show()

# Überprüfung der Tasteneingabe
def check_buttons():
    if not button_1.value():
        return 1
    elif not button_2.value():
        return 2
    elif not button_3.value():
        return 3
    else:
        return None

# Anzeige des Menüs und Auswahl des Spiels
def select_game():
    show_menu()

    while True:
        selection = check_buttons()
        if selection:
            return selection
        time.sleep(0.1)

# Starten des ausgewählten Spiels
def start_game(game):
    if game == 1:
        import snake
        snake.run_game() # Annahme, dass snake.py eine Funktion run_game() enthält, um das Spiel zu starten
    elif game == 2:
        import arcade
        arcade.run_game() # Annahme, dass arcade.py eine Funktion run_game() enthält, um das Spiel zu starten
    elif game == 3:
        import flappy
        flappy.run_game()

        
# Initialisierung der Tasten
button_1 = Pin(5, Pin.IN, Pin.PULL_UP)
button_2 = Pin(7, Pin.IN, Pin.PULL_UP)
button_3 = Pin(21, Pin.IN, Pin.PULL_UP)
button_4 = Pin(6, Pin.IN, Pin.PULL_UP)

# Auswahl des Spiels
game_selection = select_game()
start_game(game_selection)


# OLED-Spielmenü

Ein einfaches Python-Skript für MicroPython, das es ermöglicht, ein Spielmenü auf einem OLED-Display zu navigieren und Spiele wie Snake, Breakout oder Flappy zu starten. Das Skript wurde für die Verwendung mit ESP8266 oder ESP32 Mikrocontrollern konzipiert.

## Funktionen

- Anzeige eines Spielmenüs auf einem OLED-Display.
- Navigation im Menü über angeschlossene Tasten.
- Auswahl und Start verschiedener Spiele: Snake, Breakout, Flappy (und weitere in Entwicklung).

## Voraussetzungen

- Ein ESP8266 oder ESP32 Mikrocontroller.
- Ein OLED-Display, das über I2C kommuniziert (getestet mit dem SSD1306 OLED-Display).
- Vier Tasten für die Navigation im Menü.

## Verdrahtung

| OLED Pin | ESP Pin |
|----------|---------|
| SDA      | GPIO 8  |
| SCL      | GPIO 9  |

| Tasten | ESP Pin |
|--------|---------|
| UP     | GPIO 5  |
| DOWN   | GPIO 7  |
| LEFT   | GPIO 21 |
| RIGHT  | GPIO 6  |

## Installation

1. Laden Sie die neueste Version von MicroPython auf Ihren Mikrocontroller: [MicroPython Downloads](https://micropython.org/download/).
2. Kopieren Sie dieses Skript und die zugehörigen Spiel-Skripte (`snake.py`, `arcade.py`, `flappy.py`) auf Ihren Mikrocontroller.
3. Verbinden Sie das OLED-Display und die Tasten gemäß der Verdrahtungstabelle.

## Benutzung

Starten Sie das Gerät neu, um das Skript auszuführen. Das Spielmenü sollte auf dem OLED-Display erscheinen. Verwenden Sie die Tasten, um durch das Menü zu navigieren und ein Spiel auszuwählen. Das ausgewählte Spiel wird automatisch gestartet.

## Beitrag

Beiträge sind willkommen! Falls Sie eine Idee für ein neues Spiel haben oder Verbesserungen vorschlagen möchten, zögern Sie nicht, einen Pull Request zu erstellen oder ein Issue zu eröffnen.

## Lizenz

Dieses Projekt ist unter der MIT Lizenz lizenziert - siehe die [LICENSE](LICENSE.md) Datei für Details.

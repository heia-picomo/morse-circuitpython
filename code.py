import time

import board
import displayio
import picomo
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from morse import MorseCode

timeUnit = 0.1


def dit():
    picomo.led.set((255, 255, 255))
    picomo.buzzer.play(timeUnit)
    picomo.led.set((0, 0, 0))
    time.sleep(timeUnit)


def dah():
    picomo.led.set((255, 255, 255))
    picomo.buzzer.play(3 * timeUnit)
    picomo.led.set((0, 0, 0))
    time.sleep(timeUnit)


def send(m, message):
    c = m.encode(message)
    for i in c:
        if i == ".":
            dit()
        elif i == "-":
            dah()
        elif i == " ":
            time.sleep(2 * timeUnit)
        elif i == "/":
            time.sleep(6 * timeUnit)


def main():
    display = board.DISPLAY
    group = displayio.Group()
    group.append(picomo.logo)
    display.root_group = group

    mainGroup = displayio.Group()

    buttons = ["sw_up", "sw_left", "sw_mid", "sw_right", "sw_down"]
    buttons_icn = ["/pico_buttons_" + i + ".bmp" for i in ["t", "l", "c", "r", "b"]]
    messages = ["SOS", "Bonjour", "Oui", "Non", "Salut Jacques"]

    y0 = 45
    dy = 45

    for i, b in enumerate(buttons_icn):
        bitmap = displayio.OnDiskBitmap(b)
        mainGroup.append(
            displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, y=y0 + dy * i)
        )

    lucida = bitmap_font.load_font("/fonts/luRS12.bdf")
    mainGroup.append(
        Label(lucida, text="Transmetteur Morse", color=0xFFFFFF, x=35, y=20)
    )

    for i, m in enumerate(messages):
        mainGroup.append(
            Label(lucida, text=m, color=0xFFFFFF, x=40, y=y0 + dy * i + 15)
        )

    display.root_group = mainGroup

    m = MorseCode()

    btn = "sw_up"
    while True:
        picomo.update()
        for i, b in enumerate(buttons):
            if picomo.buttons[b].fell:
                send(m, messages[i])
                break

main()

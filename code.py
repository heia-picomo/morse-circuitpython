# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
Morse Code Transmitter
"""

import time

import board
import displayio
import picomo
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.line import Line
from adafruit_display_text.label import Label
from morse import MorseCode

time_unit = 0.1

messages = [
    "Yes",  # up,
    "No",  # left,
    "SOS",  # middle
    "I Love CS",  # right
    "Hello",  # down
]


buttons = ["sw_up", "sw_left", "sw_mid", "sw_right", "sw_down"]


def draw_keypad(group, x, y, r, sel):
    d = int(2.5 * r)
    for i, (xi, yi) in enumerate(
        [(x, y), (x + d, y), (x - d, y), (x, y - d), (x, y + d)]
    ):
        fill = 0xFF3333 if i == sel else 0x666666
        circle = Circle(xi, yi, r, fill=fill, outline=0xFFFFFF)
        group.append(circle)


def dit():
    picomo.led.set((255, 255, 255))
    picomo.buzzer.play(time_unit)
    picomo.led.set((0, 0, 0))
    time.sleep(time_unit)


def dah():
    picomo.led.set((255, 255, 255))
    picomo.buzzer.play(3 * time_unit)
    picomo.led.set((0, 0, 0))
    time.sleep(time_unit)


def send(m, message):
    c = m.encode(message)
    for i in c:
        if i == ".":
            dit()
        elif i == "-":
            dah()
        elif i == " ":
            time.sleep(2 * time_unit)
        elif i == "/":
            time.sleep(6 * time_unit)


def main():
    display = board.DISPLAY
    group = displayio.Group()
    group.append(picomo.logo)
    display.root_group = group

    main_group = displayio.Group()

    x0 = 24
    y0 = 65
    dy = 45

    main_group.append(Line(0, 35, display.width, 35, 0xFFFFFF))

    for i, k in enumerate([3, 2, 0, 1, 4]):
        draw_keypad(main_group, x0, y0 + i * dy, 5, k)

    lucida = bitmap_font.load_font("/fonts/luRS12.bdf")
    main_group.append(
        Label(lucida, text="Morse-Transmitter", color=0xFFFFFF, x=35, y=20)
    )

    for i, m in enumerate(messages):
        main_group.append(Label(lucida, text=m, color=0xFFFFFF, x=50, y=y0 + dy * i))

    display.root_group = main_group

    m = MorseCode()

    while True:
        picomo.update()
        for i, b in enumerate(buttons):
            if picomo.buttons[b].fell:
                send(m, messages[i])
                break


main()

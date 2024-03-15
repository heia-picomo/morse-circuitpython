################################################################################
# @brief       : Morse Code Generator for PicoMo
# @author      : Jacques Supcik <jacques.supcik@hefr.ch>
# @date        : 13. March 2024
# ------------------------------------------------------------------------------
# @copyright   : Copyright (c) 2024 HEIA-FR / ISC
#                Haute école d'ingénierie et d'architecture de Fribourg
#                Informatique et Systèmes de Communication
# @attention   : SPDX-License-Identifier: MIT
################################################################################

import time

import board
import displayio
import picomo
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from morse import MorseCode

time_unit = 0.1

messages = [
    "SOS",  # en haut,
    "Bonjour",  # à gauche,
    "Oui",  # au milieu
    "Non",  # à droite
    "HEIA",  # en bas
]


buttons = ["sw_up", "sw_left", "sw_mid", "sw_right", "sw_down"]
buttons_icn = ["/pico_buttons_" + i + ".bmp" for i in ["t", "l", "c", "r", "b"]]


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

    y0 = 45
    dy = 45

    for i, b in enumerate(buttons_icn):
        bitmap = displayio.OnDiskBitmap(b)
        main_group.append(
            displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, y=y0 + dy * i)
        )

    lucida = bitmap_font.load_font("/fonts/luRS12.bdf")
    main_group.append(
        Label(lucida, text="Transmetteur Morse", color=0xFFFFFF, x=35, y=20)
    )

    for i, m in enumerate(messages):
        main_group.append(
            Label(lucida, text=m, color=0xFFFFFF, x=40, y=y0 + dy * i + 15)
        )

    display.root_group = main_group

    m = MorseCode()

    while True:
        picomo.update()
        for i, b in enumerate(buttons):
            if picomo.buttons[b].fell:
                send(m, messages[i])
                break


main()

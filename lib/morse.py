################################################################################
# @brief       : Morse Code Encoder
# @author      : Jacques Supcik <jacques.supcik@hefr.ch>
# @date        : 13. March 2024
# ------------------------------------------------------------------------------
# @copyright   : Copyright (c) 2024 HEIA-FR / ISC
#                Haute école d'ingénierie et d'architecture de Fribourg
#                Informatique et Systèmes de Communication
# @attention   : SPDX-License-Identifier: MIT
################################################################################


class MorseCode:
    code = {  # noqa: RUF012
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        "0": "-----",
        ", ": "--..--",
        ".": ".-.-.-",
        "?": "..--..",
        "/": "-..-.",
        "-": "-....-",
        "(": "-.--.",
        ")": "-.--.-",
    }

    def __init__(self):
        pass

    def encode(self, message):
        encoded = ""
        for letter in message:
            if letter != " ":
                if letter.upper() in self.code:
                    encoded += self.code[letter.upper()] + " "
            else:
                encoded += "/"
        return encoded

import random as r
import emoji

R_EATING = f"I only like eating your brain ! {emoji.emojize(':face_with_tears_of_joy:')}"
NAME = f"Sorry, my creators Tanmai and Anjana did not name me ! {emoji.emojize(':beaming_face_with_smiling_eyes:')}"
EXIT = f"Goodbye! Glad I could help ! If you ever need help, just ask {emoji.emojize(':waving_hand:')}"
HELP = "Sure! What do you need help with ?"


def unknown():
    response = ["What does that mean ?",
                "Sorry, I didn't get you",
                "Could you please rephrase that ?"][r.randrange(3)]
    return response

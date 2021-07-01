import sys
import fc
from colors_const import COLOR_NAMES_TO_HEX
sys.path.append("../../phrase_pair_db")
import database

from PIL import Image, ImageDraw, ImageFont, ImageColor
from image_utils import ImageText
import os
import os.path
import pathlib

# Canvas.
fc_sz = [1080, 1920]

# Title
title = 'Estudos'

# Sentences
sentences = [
    "There's a group of people at the restaurant.",
    "Há um grupo de pessoas no restaurante.",
    "I don't enjoy running.",
    "Eu não curto correr.",
    "I like listening to guitar music.",
    "Eu gosto de ouvir música de violão.",
    "Where do you go fishing?",
    "Onde você vai pescar?",
    "Do you like playing soccer?",
    "Você gosta de jogar futebol?",
    "Some of the girls play with dolls.",
    "Algumas das meninas brincam com bonecas.",
    "Where do you go swimming?",
    "Onde você vai nadar?",
    "I enjoy fishing with them.",
    "Eu curto pescar com eles.",
    "A dancing group.",
    "Um grupo de dança.",
    "Some of my friends go dancing every week.",
    "Alguns dos meus amigos vão dançar toda semana.",
]
"""
def render_colors_test(color_name=None, color_hex=None):"""
    # Render colors tests, if color render one card, else, render all colors
"""
    if color_name:
        card = FlashCard((1080, 1920), title, foreign, native)
        card.card_colors(colors_dict[color_name][0], colors_dict[color_name][1])
        card.generate_bg()
        dir_name = pathlib.PurePath(os.path.abspath("card_colors"))
        card.save(str(dir_name
                      / '0_{}_test.jpg'.format(color_name)))
    else:
        for i, color in enumerate(colors_list, 1):
            card = FlashCard((1080, 1920), title, foreign, native)
            card.card_colors(colors_dict[color][0], colors_dict[color][1])
            card.generate_bg()
            dir_name = pathlib.PurePath(os.path.abspath("card_colors"))
            card.save(str(dir_name
                      / '{}_{}_test.jpg'.format(i, color)))


def make_cards(file, color, title=None):
    # Setup card folder
    card_path = pathlib.Path(os.path.dirname(file)) / "cards"
    card_path.mkdir(exist_ok=True)

    card_name = os.path.basename(file)[10:-25]
    card_n = 0

    # Setup card file
    card_file = card_path / "{}_{}.jpg".format(card_name, str(card_n))

    workbook = openpyxl.open(file)
    sheetnames = workbook.sheetnames
    worksheet = workbook[sheetnames[0]]

    foreign = []
    native = []
    for row in worksheet.iter_rows(values_only=True):
        foreign.append(row[0])
        native.append(row[1])
    foreign = chunk(foreign, 10)
    native = chunk(native, 10)

    title = os.path.basename(os.path.dirname(file))

    for sentences in zip(foreign, native):
        print("=" * 50)
        card_n += 1
        card = FlashCard(fc_sz, title, sentences[0], sentences[1], card_number=card_n)
        card.card_colors(colors_dict[color][0], colors_dict[color][1])
        card.generate_bg()
        card.save(card_path / "{}_card_{}_{}.jpg".format(str(card_n), color, card_name))
        print("=" * 50)
"""


def riffle_shuffle(lst1, lst2):
    """Riffle shuffles two list into one.

    One of each in order in a new list.
    """
    if len(lst1) != lst2:
        raise AttributeError("Lists must have the same length")
    new_list = []
    for pair in zip(lst1, lst2):
        new_list.append(pair[0])
        new_list.append(pair[1])
    return new_list


orange = fc.FCColor.from_list(COLOR_NAMES_TO_HEX["Orange"])
fc = fc.FlashCard(fc_sz, orange, title, sentences)
fp = "../out/flash_card_out.jpg"
fc.save(fp)

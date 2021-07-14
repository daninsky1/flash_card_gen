import fc
from colors_const import COLOR_NAMES_TO_HEX

# TODO: update colors test/examples
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
    """Riffle shuffles two list in a new list."""
    if len(lst1) != lst2:
        raise AttributeError("Lists must have the same length")
    new_list = []
    for pair in zip(lst1, lst2):
        new_list.append(pair[0])
        new_list.append(pair[1])
    return new_list


# Our data
title = "Simple Past Tense"
sentences = [
    "I saw a movie yesterday.",
    "Eu assisti um filme ontem.",
    "I watched movie last night.",
    "Eu assisti filme ontem à noite.",
    "Last year, I traveled to Japan.",
    "Ano passado, eu viajei para o Japão",
    "Last year, I didn't travel to South Korea.",
    "No ano passado, não viajei para a Coréia do Sul.",
    "Did you have dinner last night?",
    "Você jantou ontem à noite?",
    "She washed her car.",
    "Ela lavou o carro dela.",
    "I finished work.",
    "Eu terminei o trabalho.",
    "I lived in Brazil for 25 years.",
    "Eu morei no Brasil por 25 anos.",
    "It rained yesterday.",
    "Choveu ontem.",
    "They didn't live in Canada.",
    "Eles não moram no Canada."
]
# FCColor
color = fc.FCColor.from_list(COLOR_NAMES_TO_HEX["Forest"])
# FlashCard
fc = fc.FlashCard(title, sentences, color)
fp = "../examples/fc_example.jpg"
fc.save(fp)

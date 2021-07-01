# Canvas.
size = [1080, 1920]

# Colors.
# Name convention:
# Describe the color like a class e.g. LightBlue.
# Describe the overall color or
# title color followed by the first and sec color
# separeted by underscore e.g. Green_DarkBlue_Cyan.
#(((title_fill), (foreign_fill_color), (native_fill_color)), ((title_color), (text_color)))




colors_list = list(colors_dict)


color = "White"

# Title
title = 'Estudos'

# Sentences
foreign = [
	"There's a group of people at the restaurant.",
	"I don't enjoy running.",
	"I like listening to guitar music.",
	"Where do you go fishing?",
	"Do you like playing soccer?",
	"Some of the girls play with dolls.",
	"Where do you go swimming?",
	"I enjoy fishing with them.",
	"A dancing group.",
	"Some of my friends go dancing every week.",
]
native = [
	"Há um grupo de pessoas no restaurante.",
	"Eu não curto correr.",
	"Eu gosto de ouvir música de violão.",
	"Onde você vai pescar?",
	"Você gosta de jogar futebol?",
	"Algumas das meninas brincam com bonecas.",
	"Onde você vai nadar?",
	"Eu curto pescar com eles.",
	"Um grupo de dança.",
	"Alguns dos meus amigos vão dançar toda semana.",
]

def render_colors_test(color_name=None, color_hex=None):
	"""
	Render colors tests, if color render one card, else, render all colors
	"""
	if color_name:
		card = Card((1080, 1920), title, foreign, native)
		card.card_colors(colors_dict[color_name][0], colors_dict[color_name][1])
		card.generate_bg()
		dir_name = pathlib.PurePath(os.path.abspath("card_colors"))
		card.save(str(dir_name
					  / '0_{}_test.jpg'.format(color_name)))
	else:
		for i, color in enumerate(colors_list, 1):
			card = Card((1080, 1920), title, foreign, native)
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
		card = Card((1080, 1920), title, sentences[0], sentences[1], card_number=card_n)
		card.card_colors(colors_dict[color][0], colors_dict[color][1])
		card.generate_bg()
		card.save(card_path / "{}_card_{}_{}.jpg".format(str(card_n), color, card_name))
		print("=" * 50)


from fc_jpg import Card

# make_cards(
# 	r"C:\Users\daniel\EstudosLivros\English Language\Duolingo Frases\Torre 2\04 - Atividades 3\condensed_ Atividades 3.xlsx",
# "DarkGreen", title="foda-se")
# def test():
# 	color_i = 0
#
# 	paths = sheet_utils.get_file_path(".xlsx", start_with="condensed_")
# 	for path in paths:
# 		print(path)
# 		make_cards(path, colors_list[color_i])
# 		color_i += 1

render_colors_test(color_name=colors_list[-1])

# for theme in basico_theme_list:
# 	print(colors_dict[basico_theme_dict[theme]])


"""
MIT License

Copyright (c) 2020 Daniel Silva dos Santos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageColor
from image_utils import ImageText
import colors_const
import colour
import piexif
import os
import os.path
import pathlib


class FCColor:
    def __init__(self, title_box_color, text_box_color1, text_box_color2,
                 title_text_color, text_color):
        """
        :param title_box_color: A color string
        :param text_box_color1: A color string
        :param text_box_color2: A color string
        :param title_text_color: A color string
        :param text_color: A color string
        """
        self.title_box_color = ImageColor.getrgb(title_box_color)
        self.text_box_color1 = ImageColor.getrgb(text_box_color1)
        self.text_box_color2 = ImageColor.getrgb(text_box_color2)
        self.title_text_color = ImageColor.getrgb(title_text_color)
        self.text_color = ImageColor.getrgb(text_color)

    @classmethod
    def from_list(cls, color_list):
        """From list or tuple"""
        if not isinstance(color_list, list) and not isinstance(color_list, tuple):
            raise TypeError("color_list be a tuple or list.")

        if len(color_list) == 2:
            if not isinstance(color_list[0], list) and not isinstance(color_list[0], tuple) and \
                    isinstance(color_list[1], list) and not isinstance(color_list[1], tuple):
                raise TypeError("First and second color_list elements must be a tuple or list.")
            elif len(color_list[0]) != 3 or len(color_list[1]) != 2:
                raise ValueError("First color_list list element must have 3 hex color elements.\n"
                                 "And second color_list list element must have 2 hex color elements.")
            return cls(color_list[0][0], color_list[0][1], color_list[0][2], color_list[1][0], color_list[1][1])
        elif len(color_list) == 5:
            return cls(color_list[0], color_list[1], color_list[2], color_list[3], color_list[4])


class FlashCard:
    """Card generates a flash card jpg and fodg."""

    def __init__(self, fc_sz, card_color=None, title=None, sentences=None, card_number=None):
        if not isinstance(fc_sz, list) and not isinstance(fc_sz, tuple):
            raise TypeError('size must be a tuple or list')
        if len(fc_sz) != 2:
            raise AttributeError('size must have 2 coordinate values xy')


        # Flash card and boxes sizes
        self.fc_sz = fc_sz
        self.w, self.h = fc_sz
        self.title_box_sz = [self.w, 174]  # px
        # Height division areas for text boxes and text
        self.div_text_box = list(range(self.title_box_sz[1], self.h, round(self.h / 22)))

        # Flash card appearance
        self.card_color = self.set_color(card_color)
        self.title_font = "../fonts/JosefinSans-Bold.ttf"
        self.text_font1 = "../fonts/JosefinSans-Bold.ttf"
        self.text_font2 = "../fonts/JosefinSans-Regular.ttf"

        # Flash card text data
        self.title = title
        self.sentences = sentences
        self.card_number = card_number

        # Flash card
        self.flash_card = None

        # TODO: set the future of exif info
        # Exif info.
        zeroth_ifd = {
            piexif.ImageIFD.Artist: u"Daninsky, Daniel Silva dos Santos",
            piexif.ImageIFD.Software: u"Duo Breaker script",
            piexif.ImageIFD.Copyright: u"(CC BY 4.0) Attribution 4.0 International",
            piexif.ImageIFD.XPComment: "Phrases from duolingo.com scraped with Duo Breaker script. /"
                                       "@danieldaninsky, @Daninsky, @Daninsky12".encode("utf-16"),
            piexif.ImageIFD.XPAuthor: "Daninsky".encode("utf-16")
        }
        exif_dict = {"0th": zeroth_ifd}
        self.exif_bytes = piexif.dump(exif_dict)

    def set_color(self, card_color=None):
        """Set flash card color.

        :param card_color: FCColor
        :return: void
        """
        if card_color is None:
            card_color = FCColor.from_list(colors_const.COLOR_NAMES_TO_HEX["Black_DarkSlateGray_SlateGray"])
        elif not isinstance(card_color, FCColor):
            raise TypeError("card_color must be FCColor")
        self.card_color = card_color

    def draw_bg(self):
        """Draw flash card background."""
        if self.flash_card is None:
            self.flash_card = Image.new("RGB", self.fc_sz, self.bg_secon_color)
        draw = ImageDraw.Draw(self.flash_card)
        title_box = [0, 0, self.title_box_sz[0], self.title_box_sz[1]]
        draw.rectangle(title_box, fill=self.bg_title_color)

        for chunk in self.div_H1_chunks:
            draw.rectangle(((0, chunk[0]), (self.w, chunk[1])), fill=self.bg_first_color)

        fnt = ImageFont.truetype(self.reg_font, 25)
        fnt2 = ImageFont.truetype(self.reg_font, 40)
        n_size = fnt2.getsize(str(self.card_number))[0]
        draw.text((15, 15), "@danieldaninsky", font=fnt, fill=self.font_title_color)
        if self.card_number:
            draw.text(((self.w - (30 + n_size)), 30), str(self.card_number), font=fnt2, fill=self.font_title_color)

    def draw_title(self):
        """Draw flash card title."""
        if self.flash_card is None:
            self.flash_card = Image.new('RGB', self.fc_sz, self.color[0][1])
        txt = ImageText(self.flash_card)
        txt.write_text_box((0, 0), self.title, box_width=self.w,
                           font_filename=self.bold_font, font_size=80,
                           color=self.font_title_color,
                           place='center', height_compensations=(60, 0, 0))

    def draw_sentences(self):
        """Draw flash card sentences"""
        if self.flash_card is None:
            self.flash_card = Image.new('RGB', self.fc_sz, self.bg_secon_color)
        txt = ImageText(self.flash_card)
        all_sentences = []

        for sentence in self.sentences:
            all_sentences.append(sentence[0])
            all_sentences.append(sentence[1])

        fnt = self.text_font1
        count = 0
        for i, sentence in enumerate(all_sentences):
            count += 1
            print(count, " - ", sentence)
            txt.write_text_box((0, self.div_text_box[i]), sentence,
                               box_width=self.w,
                               font_filename=fnt,
                               font_size=42, font_min_size=34,
                               color=self.font_sente_color,
                               place='center', height_compensations=(26, 30, 12))
            fnt = self.text_font2 if fnt == self.text_font1 else fnt = self.text_font1

    def __draw_all(self):
        """Draw all flash card elements."""
        self.card_color()
        self.draw_bg()
        self.draw_title()
        self.draw_sentences()

    def save(self, path):
        if self.flash_card is None:
            self.__draw_all()
        else:
            print("Warning: Calling any draw method will disable the automatic call to __draw_all().")
        self.draw_sentences().save(path, exif=self.exif_bytes)


if __name__ == '__main__':
    pass
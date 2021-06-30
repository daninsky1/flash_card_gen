import xml.etree.ElementTree as ET
import fc_jpg
import copy
import utils
import os
import os.path
import pathlib

ns = {
    "officeooo": "http://openoffice.org/2009/office",
    "anim": "urn:oasis:names:tc:opendocument:xmlns:animation:1.0",
    "smil":"urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0",
    "number": "urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0",
    "rpt": "http://openoffice.org/2005/report",
    "chart": "urn:oasis:names:tc:opendocument:xmlns:chart:1.0",
    "svg": "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
    "dr3d": "urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0",
    "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    "drawooo": "http://openoffice.org/2010/draw",
    "style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
    "meta": "urn:oasis:names:tc:opendocument:xmlns:meta:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "ooo": "http://openoffice.org/2004/office",
    "xlink": "http://www.w3.org/1999/xlink",
    "loext": "urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0",
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "dc": "http://purl.org/dc/elements/1.1/",
    "fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
    "calcext": "urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "tableooo": "http://openoffice.org/2009/table",
    "config": "urn:oasis:names:tc:opendocument:xmlns:config:1.0",
    "of": "urn:oasis:names:tc:opendocument:xmlns:of:1.2",
    "ooow": "http://openoffice.org/2004/writer",
    "field": "urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0",
    "math": "http://www.w3.org/1998/Math/MathML",
    "form": "urn:oasis:names:tc:opendocument:xmlns:form:1.0",
    "script": "urn:oasis:names:tc:opendocument:xmlns:script:1.0",
    "dom": "http://www.w3.org/2001/xml-events",
    "xforms": "http://www.w3.org/2002/xforms",
    "oooc": "http://openoffice.org/2004/calc",
    "formx": "urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi":"http://www.w3.org/2001/XMLSchema-instance",
    "css3t": "http://www.w3.org/TR/css3-text/",
    "xhtml": "http://www.w3.org/1999/xhtml",
    "grddl": "http://www.w3.org/2003/g/data-view#",
    "presentation": "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
    "version": "1.2",
    "mimetype": "application/vnd.oasis.opendocument.graphics"
}


def register_all_ns(ns_file_path):
    """
    Registra o namespaces antes de salvar, porque o filha da puta que escreveu essa
    biblioteca fumou muito crack pra fazer isso se comportar de forma tão esquisofrenica.
    Ele salva com namespace só arquivos que ele acha legal. O resto pau no cú, têm que
    se virar para descobrir como salvar seus default namespaces.
    """
    namespaces = dict([node for _, node in ET.iterparse(ns_file_path, events=["start-ns"])])
    for ns in namespaces:
        ET.register_namespace(ns, namespaces[ns])


def config_xml_file(xml_file):
    """
    Setup the page blocks
    """

    tree = ET.ElementTree(file=xml_file)
    root = tree.getroot()

    auto_styles = root[5]

    # Add graphic styles "colors"
    gr_style = auto_styles[3]   # Steal gr_style element
    # auto_styles.remove(gr_style)  # Remove original gr_style template
    gr_fill = gr_style[0]

    for color_set in fc_jpg.colors_list:
        for n, color in enumerate(fc_jpg.colors_dict[color_set][0]):
            gr_style.set('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name',
                         str(n) + "_" + color_set)
            #  + "_" + color.lower()
            gr_fill.set('{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}fill-color',
                        color.lower())
            cpy = copy.deepcopy(gr_style)   # Needs to be a copy or else will append a istance
            # print(str(n) + "_" + color_set + "_" + color.lower())
            # print(gr_style.attrib, fill.attrib)
            auto_styles.append(cpy)


    # Add text styles
    title_style = auto_styles[14]
    title_fill = title_style[0]
    bold_style = auto_styles[15]
    bold_fill = bold_style[0]
    regular_style = auto_styles[16]
    regular_fill = regular_style[0]

    auto_styles.remove(title_style)
    auto_styles.remove(bold_style)
    auto_styles.remove(regular_style)

    for color_set in fc_jpg.colors_list:
        title_color = fc_jpg.colors_dict[color_set][1][0]
        txt_color = fc_jpg.colors_dict[color_set][1][1]

        # Title style
        title_style.set('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name',
                        "title_" + color_set)
        title_fill.set('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}color',
                       title_color.lower())
        cpy = copy.deepcopy(title_style)   # Needs to be a copy or else will append a istance
        auto_styles.append(cpy)

        # Bold style
        bold_style.set('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name',
                        "bold_" + color_set)
        bold_fill.set('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}color',
                       txt_color.lower())
        cpy = copy.deepcopy(bold_style)   # Needs to be a copy or else will append a istance
        auto_styles.append(cpy)

        # Regular style
        regular_style.set('{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name',
                        "regular_" + color_set)
        regular_fill.set('{urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0}color',
                       txt_color.lower())
        cpy = copy.deepcopy(regular_style)   # Needs to be a copy or else will append a istance
        auto_styles.append(cpy)


    # Config one page
    # Add pages and its links to graphic style and text style, and title, and phrases
    drawing = root[7][0]
    page = drawing[0]
    drawing.remove(page)

    title_box = page[0]
    title_text = title_box[0][0]

    native_group = page[1]
    foreign_group = page[2]

    color_name = "Brazil"

    # Title config
    title_box.set('{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name',
                  "0_" + color_name)
    txt_tag = title_box[0][0]
    txt_tag.set('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name',
                 "title_" + color_name)
    title_text.text = ""

    # Foreign bold config
    for custom_shape in foreign_group:
        # style_name = phrase.find("draw:style-name", namespaces=ns)
        custom_shape.set('{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name',
                   "1_" + color_name)   # style_attribute
        txt_tag = custom_shape[0][0][0][0]
        txt_tag.set('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name',
                     "bold_" + color_name)
        txt_tag.text = ""  # Erase any previews text

    # Native regular config
    for custom_shape in native_group:
        custom_shape.set('{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name',
                   "2_" + color_name)  # style_attribute
        txt_tag = custom_shape[0][0][0][0]
        txt_tag.set('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name',
                     "regular_" + color_name)
        txt_tag.text = ""  # Erase any previews text

    cpy = copy.deepcopy(page)
    drawing.append(cpy)

    register_all_ns(xml_file)
    tree.write("/mnt/windows/Users/daniel/EstudosLivros/Python/06 - sheet and card sort creator/xml_blocks/pageConfig.fodg", encoding="utf-8",
               xml_declaration=True)



def make_page(color_name, title, phrases):
    """
    :param color_set: str color name that was defined early in the code,
    colors defined in the cardgenerator.color_list list
    :param phrases: list of translations e.g.:
    (("one", "two", "three"), ("um", "dois", "três"))
    :param title:
    :return:
    """

    tree = ET.ElementTree(file="/mnt/windows/Users/daniel/EstudosLivros/Python/06 - sheet and card sort creator/xml_blocks/pageConfig.fodg")
    root = tree.getroot()

    # Add pages and its links to graphic style and text style, and title, and phrases
    drawing = root[7][0]
    page = drawing[0]
    drawing.remove(page)

    title_box = page[0]
    title_text = title_box[0][0]

    native_group = page[1]
    foreign_group = page[2]

    if not isinstance(phrases, list) and not isinstance(phrases, tuple):
        raise ValueError("It must be list or tuple!")
    if len(phrases) != 2:
        raise ValueError("It must be two lists with up to 10 phrases!")
    if len(phrases[0]) != len(phrases[1]):
        raise ValueError("the number of sentences of the translation must be equal!")
    if len(phrases[0]) == 0:
        raise Exception("The lists are empty!")


    # Link colors and styles
    title_box.set('{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name',
                  "0_" + color_name)
    txt_tag = title_box[0][0]
    txt_tag.set('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name',
                 "title_" + color_name)
    title_text.text = title

    phrase_i = 0

    # Foreign bold text
    for custom_shape in foreign_group:
        # style_name = phrase.find("draw:style-name", namespaces=ns)
        custom_shape.set('{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name',
                   "1_" + color_name)   # style_attribute
        txt_tag = custom_shape[0][0][0][0]
        txt_tag.set('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name',
                     "bold_" + color_name)
        # Look out this is broken
        try:
            txt_tag.text = phrases[0][phrase_i]
            phrase_i += 1
        except IndexError:
            txt_tag.text = ""   # Erase any previews text

    phrase_i = 0

    # Native regular text
    for custom_shape in native_group:
        custom_shape.set('{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name',
                   "2_" + color_name)  # style_attribute
        txt_tag = custom_shape[0][0][0][0]
        txt_tag.set('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name',
                     "regular_" + color_name)
        try:
            txt_tag.text = phrases[1][phrase_i]
            phrase_i += 1
        except IndexError:
            txt_tag.text = ""  # Erase any previews text

    return copy.deepcopy(page)



def append_pages(xml_out, pages):
    xml_in = "/mnt/windows/Users/daniel/EstudosLivros/Python/06 - sheet and card sort creator/xml_blocks/pageConfig.fodg"
    tree = ET.ElementTree(file=xml_in)
    root = tree.getroot()

    # Add pages and its links to graphic style and text style, and title, and phrases
    drawing = root[7][0]
    page = drawing[0]
    drawing.remove(page)
    page_n = 1
    for page in pages:
        page.set('{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name',
                 "page{}".format(page_n))
        page_n += 1
        drawing.append(page)

    register_all_ns(xml_in)
    tree.write(xml_out, encoding="utf-8",
               xml_declaration=True)


def make_all(file_path, file_path_out=None):
    config_xml_file("/mnt/windows/Users/daniel/EstudosLivros/Python/06 - sheet and card sort creator/xml_blocks/pageGmod.fodg")

    if not isinstance(file_path, pathlib.PurePosixPath) and not isinstance(file_path, pathlib.PureWindowsPath):
        file_path = pathlib.PurePath(file_path)

    i = 0
    pages = []
    index_title = {}
    index_phrase = {}
    index_color = {}
    for path in utils.get_file_path(
            "xlsx", start_with="condensed_",
            path=file_path,
    ):
        index = utils.read_n_spit(path, mode=3)
        title = os.path.basename(os.path.dirname(path))
        index_title[index] = title

        phrases = utils.read_n_spit(path, length=10)
        index_phrase[index] = phrases

        color_name = utils.read_n_spit(path, mode=2)
        index_color[index] = color_name

    index_sort = sorted(list(index_title))
    # print(index_phrase[1])
    for n in index_sort:
        for phrase in index_phrase[n]:
            pages.append(make_page(index_color[n], index_title[n], phrase))

    # Save file
    if file_path_out:
        append_pages(file_path_out, pages)
    else:
        append_pages(file_path
                     / "{}.fodg".format(str(os.path.basename(file_path))),
                     pages)


if __name__ == "__main__":
    # main_path = pathlib.PurePath(
    #     "/mnt/windows/Users/daniel/EstudosLivros/English Language/Duolingo Frases"
    # )
    # main_path_list = ["Básico", "Torre 1", "Torre 2", "Torre 3",
    #             "Torre 4", "Torre 5", "Torre 6"]
    # for n,path in enumerate(main_path_list):
    #     make_all(main_path / main_path_list[n])

    make_all("/mnt/windows/Users/daniel/EstudosLivros/English Language/Duolingo Frases/V0.1/Básico")

    # path = pathlib.PurePath("/mnt/windows/Users/daniel/EstudosLivros/English Language/Duolingo Frases")
    # print(type(path))
    # print(isinstance(path, pathlib.PurePosixPath))
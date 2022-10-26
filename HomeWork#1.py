
"""

import os
import re
import schutil

# створюємо словник відомих розширень. ключ то назва типу, значення то кортеж розширень
EXTENSION_DICT = {
    'archives': ('zip', 'gz', 'tar'),
    'video': ('avi', 'mp4', 'mov', 'mkv'),
    'audio': ('mp3', 'ogg', 'wav', 'amr'),
    'docs': ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx', 'xls', 'xlsx', 'docx'),
    'images': ('png', 'jpg', 'svg', 'jpeg'),
    'draws': ('dwg', 'dxf')
}

# ввідні дані для транслітерації.
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}  # створюємо словник перекладу.
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


BASE_DIR = ''


def normalize(item: str) -> str:
    """ ф-ція яка "нормалізує"/перекладає назву з кирилиці на латиницю і змінює всі символі на "_" """
    # замінюємо всі символи на інший символ
    name_file = re.sub(r"\W", "_", item, flags=re.IGNORECASE)
    # переклад назви відповідно до словнику на який посилаємось
    return name_file.translate(TRANS)


def work_f(name, file_path):
    """ Ф-ція ___ яка створює диерктокрію, якщо її немає і переміщує туди файли з вказаним розиренням"""
    name_path = os.path.join(BASE_DIR, name)
    if not os.path.exists(name_path):  # створюємо папку, якщо її немає
        os.mkdir(name_path)
    new_file = os.path.join(name_path, os.path.basename(
        file_path
    ))  # створюємо шлях для нового файлу
    os.replace(file_path, new_file)  # переміщуємо файл


def sort(file_path):
    """ф-ція сортування"""
    for type_, exts in EXTENSION_DICT.items():
        if file_path.lower().endswith(exts):
            work_f(type_, file_path)
            break
    else:
        work_f('unknowns', file_path)


def in_folder(dir_path):
    """ф-ція проходу проходу по каталогу"""

    # створюємо перелік вмісту файлів та директорій всередині

    for item in os.listdir(dir_path):  # перебираюємо всі файли і забираємо їх шляхи

        # probably should sanitize this beforehand
        if item in EXTENSION_DICT.keys():
            continue

        # створюємо шлях до файлу\директорії
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):  # якщо директорія то
            new_name = os.path.join(dir_path, normalize(item))
            os.rename(item_path, new_name)
            in_folder(new_name)  # викликаємо ф-цію аби зайтий в директорію

        elif os.path.isfile(item_path):
            name, ext = os.path.splitext(item)
            new_name = os.path.join(dir_path, normalize(name) + ext)
            os.rename(item_path, new_name)
            sort(new_name)  # сортування файлів

    if not os.listdir(dir_path):
        os.rmdir(dir_path)  # видаляэмо директорію


if __name__ == '__main__':
    dir_path = os.path.abspath('./SortFiles')
    BASE_DIR = dir_path
    in_folder(dir_path)

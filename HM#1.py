import os
import re
import shutil

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
# створюємо словник перекладу. Він буде виконуватись кожен раз за викликом.
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

# BASE_DIR - головний шлях який задається користувачем
BASE_FOLDER: Path | None = None


def in_folder(dir_path):
    """ф-ція проходу проходу по каталогу"""

    for item in os.listdir(dir_path):  # перебираюємо всі файли і забираємо їх шляхи

        # якщо назва вже є -> продовжуємо
        if item in EXTENSION_DICT():
            continue
        # створюємо шлях до директорії/файлу
        item_path = os.path.join(dir_path, item)

        if os.path.isdir(item_path):  # якщо директорія то
            # створюємо ім'я з'єднавши шлях і "нормалізовану" назву директорії
            new_name = os.path.join(dir_path, normalize(item))
            os.rename(item_path, new_name)  # замінюємо директорію
            # рекурсія виклику/викликаємо ф-цію аби зайтий в директорію
            in_folder(new_name)

        elif os.path.isfile(item_path):  # якщо файл то
            # створюємо 2 змінні, розбиваючи ім'я файлу на назву та розширення
            name, ext = os.path.splitext(item)
            # створюємо новий шлях,об'єднуючи шлях директорії, "нормалізуючи" назви та повертаємо розширення
            new_name = os.path.join(dir_path, normalize(name) + ext)
            os.rename(item_path, new_name)  # замінюємо файл
            sort(new_name)  # передаємо файл до ф-ції сорутвання

    if not os.listdir(dir_path):
        os.rmdir(dir_path)  # видаляємо директорію, якшо вона порожня


def sort(file_path):
    """ф-ція сортування"""
    # проходимо по по словнику розширень,
    for type_, exts in EXTENSION_DICT.items():
        # якщо закінчення файлу знайдене в параметрах словника
        if file_path.lower().endswith(exts):
            # викликаємо ф-ція обробки, передаючи "тип файлу" та шлях до нього
            work_f(type_, file_path)
            break
    else:  # якщо цикл повністю пройдений але не зайшли в цикл, то файл буде перенесений до
        work_f('unknowns', file_path)


def normalize(item: str) -> str:
    """ ф-ція яка "нормалізує"/перекладає назву з кирилиці на латиницю і змінює всі символі на "_" """
    # замінюємо всі символи на інший символ
    name_file = re.sub(r"\W", "_", item, flags=re.IGNORECASE)
    # переклад назви відповідно до словнику на який посилаємось
    return name_file.translate(TRANS)


def work_f(name, file_path):
    """ Ф-ція загальна яка створює диерктокрію, якщо її немає і переміщує туди файли з вказаним розширенням"""
    # створюємо повний шлях до файлу
    name_path = os.path.join(BASE_DIR, name)
    if not os.path.exists(name_path):  # створюємо директорію, якщо її немає
        os.mkdir(name_path)
    new_file = os.path.join(name_path, os.path.basename(
        file_path))  # створюємо шлях для нового файлу
    # якщо архів, то необхідно додатково обробити файл
    if name == 'archives':
        # створюжмо шлях куди будемо розпаковувати
        unpack_path = os.path.splitext(new_file)
        os.mkdir(unpack_path)  # створюємо директорію з назвою архіву
        # розпаковуємо архів по новому шляху
        shutil.unpack_archive(file_path, unpack_path)
        # видаляємо архів
        os.remove(file_path)
    else:
        os.replace(file_path, new_file)  # переміщуємо файл, бо не архів


def main():
    global BASE_FOLDER

    if len(sys.argv) < 2:
        print('Enter path')
        exit()

    BASE_DIR = Path(sys.argv[1])

    if (not BASE_DIR.exists()) or (not BASE_DIR.is_dir()):
        print('Path incorrect')
        exit()

    BASE_FOLDER = BASE_DIR
    normalize()
    in_folder(BASE_DIR)


if __name__ == '__main__':
    main()

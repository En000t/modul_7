import os
import shutil
import re
import sys


def normalize(filename):
    translit_table = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
        'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
        'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E',
        'Ю': 'Yu', 'Я': 'Ya'
    }
    filename = filename.translate(str.maketrans(translit_table))
    filename = re.sub(r'[^A-Za-z0-9_.]', '_', filename)
    return filename


def create_directories(folder, directories):
    for directory in directories:
        os.makedirs(os.path.join(folder, directory), exist_ok=True)


def sort_files(folder):
    directories = ['images', 'videos', 'documents', 'audio', 'archives', 'other']
    extensions_mapping = {
        'images': ['JPEG', 'JPG', 'PNG', 'SVG'],
        'videos': ['AVI', 'MP4', 'MOV', 'MKV'],
        'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
        'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
        'archives': ['ZIP', 'GZ', 'TAR']
    }

    create_directories(folder, directories)

    images = []
    videos = []
    documents = []
    audio = []
    archives = []
    unknown_extensions = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            _, extension = os.path.splitext(file)
            new_filename = normalize(file)

            destination_folder = None

            extension = extension[1:].upper()
            for directory, extensions in extensions_mapping.items():
                if extension in extensions:
                    destination_folder = directory
                    break
            else:
                unknown_extensions.append(new_filename)
                destination_folder = 'other'

            if destination_folder:
                shutil.move(file_path, os.path.join(folder, destination_folder, new_filename))

                if extension in ['ZIP', 'GZ', 'TAR']:
                    shutil.unpack_archive(os.path.join(folder, destination_folder, new_filename),
                                          os.path.join(folder, destination_folder))
                    os.remove(os.path.join(folder, destination_folder, new_filename))

    for root, dirs, files in os.walk(folder, topdown=False):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    return images, videos, documents, audio, archives, unknown_extensions


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python clean.py <folder>')
        sys.exit(1)

    folder = sys.argv[1]

    images, videos, documents, audio, archives, unknown_extensions = sort_files(folder)

    print('Images:')
    for image in images:
        print(image)

    print('Videos:')
    for video in videos:
        print(video)

    print('Documents:')
    for document in documents:
        print(document)

    print('Audio:')
    for song in audio:
        print(song)

    print('Archives:')
    for archive in archives:
        print(archive)

    print('Unknown Extensions:')
    for extension in unknown_extensions:
        print(extension)

if __name__ == '__main__':
    main()
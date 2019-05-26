from pathlib import Path

def bright_green (text):
    return '\033[1;32;40m{text}\033[0m'.format(text=text)

def bright_blue (text):
    return '\033[1;34;40m{text}\033[0m'.format(text=text)

def bright_red (text):
    return '\033[1;31;40m{text}\033[0m'.format(text=text)

def bright_yellow (text):
    return '\033[1;33;40m{text}\033[0m'.format(text=text)

def bold (text):
    return '\033[1m{text}\033[0m'.format(text=text)

def validate_path(path):
    db_file = Path(path)
    exists = db_file.is_file()

    if not exists:
        print(bright_red("Error: file '{p}' not found".format(p = path)))

    return exists

import re

from src.dictionary import allowed_chars, delimiters, header_pattern
from src.timer import timer


def add_delimiter_to_db(name: str, delimiter: str, db):
    cur = db.cursor()
    cur.execute('''
        UPDATE "hospitals"
        SET "delimiter" = "{}"
        WHERE name == "{}"
        '''.format(delimiter, name))
    db.commit()

@timer
def parse_easy(name: str, file: str, db) -> tuple:
    '''DETERMINE AND RETURN $header and $delimiter'''
    with open(file, 'r') as temp:
        header = None
        delimiter_count = dict()
        lines = list()
        i = int(0)
        header_index = int()
        while i < 20 and header == None:
            lines.append(temp.readline())
            if (re.search(header_pattern, lines[i])):
                # $header = Str of allowed ASCII chars, ignore others
                # header = ''.join(char for char in lines[i] if ord(char) in allowed_chars)
                header, header_index = lines[i], i
                del lines[i]
                i -= 1
            i += 1
        if header:
            for char in delimiters:
                if char in header:
                    delimiter_count[char] = header.count(char)
        try:
            # Assume max counted delimiter type is said chargemaster's delimiter
            delimiter: str = max(delimiter_count,key=lambda x: delimiter_count[x])
            add_delimiter_to_db(name=name, delimiter=delimiter, db=db)
            # Return ($delimiter, $header)
            return (
                delimiter,
                ''.join(char for char in header if ord(char) in allowed_chars).split(delimiter),
                header_index
                )
        except ValueError as ve:
            print(f'{file}\n{ve}')

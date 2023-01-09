import pandas

from src.db_conn import db_connect
from src.dictionary import reword, ROOT
from src.timer import timer


# Should I rename all columns to easier ones like `description` or
# have the flask app call the first column that matches a regex?
# @timer
def generate_easy(name: str, sheet, delimiter: str, head_index: list):
    '''
    Generate an sqlite database table from chargemasters with file
    extensions in the "easy" category [.txt, .csv].
    '''
    database = db_connect(ROOT / "chargemaster.db")
    hospital = pandas.read_csv(
        filepath_or_buffer=sheet,
        delimiter=delimiter,
        encoding='utf-8',
        encoding_errors='ignore',
        na_filter=False,
        header=head_index,
        usecols=lambda x: 'Unnamed' not in x) # lambda removes columns generated without names
    hospital.columns = hospital.columns.str.lower()
    hospital.columns = hospital.columns.str.replace(pat=r'\_', repl=' ', regex=True) # Rename troublesome columns
    hospital.replace(to_replace=r"\'| \[\d*\]|\,", value="", regex=True, inplace=True) # Remove troublesome chars
    hospital.rename(
        columns=reword,
        inplace=True) # I should probably replace dict(reword) with a function for better rename
    hospital.to_sql(name=name, con=database, index=False, if_exists='replace')

@timer
def generate_med(name: str, sheet: str):
    '''
    Generate an sqlite database table from chargemasters
    with file extensions in the "med" category.
    ([.xml, .json])
    '''
    ...

@timer
def generate_hard(name: str, sheet: str):
    '''
    Generate an sqlite database table from chargemasters
    with file extensions in the "hard" category.
    ([.pdf, .xlsx])
    Probably use pdfplumber for .pdf
    '''
    ...

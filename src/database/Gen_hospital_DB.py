import pandas

from src.db_conn import db_connect
from src.timer import timer




@timer
def gen_hospital_db():
    '''
    RETURN $hospital.db CONNECTION
    '''
    # db = sql.connect('hospital.db')
    db = db_connect('hospital.db')
    hospital = pandas.read_csv(
        'onefact_paylesshealth_main_hospitals.csv',
        encoding='utf-8',
        encoding_errors='ignore',
        na_filter=False
        )
    hospital['delimiter'] = ''
    hospital.replace(r"\'", "", regex=True, inplace=True)
    hospital.to_sql(name='hospitals', con=db, index=False, if_exists='replace')
    return db



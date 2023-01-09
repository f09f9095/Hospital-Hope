from src.dictionary import chargemaster_path, file_types, ROOT
from src.downloader import download
from src.database.Gen_chargemaster_DB import generate_easy, generate_med, generate_hard
from src.database.Gen_hospital_DB import gen_hospital_db
from src.parsers import parse_easy


'''
1.  GEN `hospital.db` AND ADD EMPTY 'delimiter' COLUMN
2.  GATHER LIST OF HOSPITALS (name,filename,url) WITH A DOWNLOAD URL
    FROM `hospital.db`
3.  DOWNLOAD MISSING CHARGEMASTERS
4.  TODO: PARSE CHARGEMASTERS TO DETERMINE $header AND $delimiter
5.  TODO: GEN TABLE IN `chargemaster.db` FOR EACH HOSPITAL
'''


def hospital_tuples(hos_db) -> list:
    '''
    Return list of tuples (name,filename,url) from `hospital.db`
    '''
    cur = hos_db.cursor()
    hospitals = cur.execute('''
        SELECT name, cdm_url FROM hospitals
        WHERE cdm_url LIKE "%.___"
        OR
        cdm_url LIKE "%.____"
        ''')
    hospitals = [(name,url.split('/')[-1],url) for name,url in hospitals.fetchall()]
    return hospitals


if __name__ == '__main__':
    '''
    1)  Generate `hospital.db` from `onefact_paylesshealth_main_hospitals.csv`
        and add empty column "delimiter". 
        Return sqlite DB connection.
    '''
    hos_db = gen_hospital_db()
    '''
    2)  Gather list of hospital (name,filename,url) from `hospital.db`
        in $chargemaster_path (src/chargemasters).
    '''
    hospitals = hospital_tuples(hos_db)

    for name, filename, url in hospitals:
        if not (sheet:=(chargemaster_path / filename)).is_file():
            '''3) Download chargemasters not present in /src/chargemasters'''
            # download(url=url, sheet=sheet)
            ...
        elif sheet.suffix in file_types['easy']:
            '''4) Parse chargemaster for $header and $delimiter'''
            parsed_tup = parse_easy(name=name, file=str(sheet), db=hos_db)
            '''5) GENERATES `chargemaster.db` AND TABLES FOR HOSPITALS
                  FROM "easy" CATEGORY'''
            generate_easy(name=name, sheet=sheet, delimiter=parsed_tup[0], head_index=parsed_tup[2])
        elif sheet.suffix in file_types['med']:
            # generate_med(name, filename, hos_db)
            ...
        elif sheet.suffix in file_types['hard']:
            # generate_hard(name, filename, hos_db)
            ...

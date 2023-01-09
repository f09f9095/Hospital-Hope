import requests

from src.timer import timer


@timer
def download(url: str, sheet: str):
    '''
    Download chargemaster from given url
    '''
    with requests.get(url, stream=True) as got, open(sheet, 'wb') as file:
        for chunk in got.iter_content(10000):
            file.write(chunk)

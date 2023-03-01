"""

"""
import os
import time
from urllib.request import urlretrieve
import requests

import pandas as pd

import unicodedata
import re
from bs4 import BeautifulSoup


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def download_file(url, save_path):
    # urlretrieve(url, 'path_to_save_plus_some_file.pdf')
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        fd.write(response.content)

    # with open(save_path, 'wb') as fd:
    #     for chunk in response.iter_content(4000):
    #         fd.write(chunk)


def download_file2(url, save_path):
    # Requests URL and get response object
    response = requests.get(url)
    # print(response.content)

    # Parse text obtained
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all hyperlinks present on webpage
    links = soup.find_all('iframe')
    print(links)
    print()


def download_all_file_pdf():
    df1 = pd.read_excel('../data/ieee_xplore_search_result_r2_all_non-duplicated.xlsx',
                        sheet_name='Sheet1')
    for i, row in df1.iterrows():
        pdf_title = row['Document Title']
        pdf_title = slugify(pdf_title)
        pdf_year = row['Publication Year']
        pdf_number = row['PDF Link'].split('=')[1]

        url = f'https://ie1.glibrary.net/stamp/stamp.jsp?tp=&arnumber={pdf_number}'
        # download_file2(url, os.path.join('../pdfs/ieee_r2', f'{pdf_year}_{pdf_title}.pdf'))
        print(url)
        print(f'article {i}: "{pdf_year}_{pdf_title}" was saved.')
        time.sleep(1)


if __name__ == '__main__':
    download_all_file_pdf()

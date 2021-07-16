import requests
import time
import re
import os
import shutil
import pickle
from urllib.parse import urljoin
from bs4 import BeautifulSoup

parent = 'https://webbook.nist.gov/'
valid = {}
invalid = {}
unavailable = []
valid_labels = ['page_url', 'download_url', 'molecular weight', 'resolution', 'state', 'is gas?']
invalid_labels = ['page_url', 'molecular_weight']

try:
    os.mkdir('Dataset')
except OSError:
    pass


def strip(string):
    return re.sub(r'\s+', '', string)


def extract_float(string):
    return float('.'.join(re.findall(r'\d+', string)))


def generate_mw_search(lbound, stride):  # lbound -> lower bound for molecular weight range, stride -> range
    return f'{parent}cgi/cbook.cgi?Value={lbound}-{lbound + stride}&VType=MW&Units=SI&cIR=on'


def generate_name_search(name):
    return f'{parent}cgi/cbook.cgi?Name={name}&Units=SI&cIR=on'.replace(' ', '+')


# noinspection PyBroadException
def parse_page(url):  # gets the download url for IR data
    start = time.time()

    soup = BeautifulSoup(requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT '
                                                                  '10.0; Win64; x64) '
                                                                  'AppleWebKit/537.36 (KHTML, '
                                                                  'like Gecko) '
                                                                  'Chrome/91.0.4472.106 '
                                                                  'Safari/537.36'}).content, 'html.parser')
    name = soup.findAll('h1')[-1].get_text()
    mw = extract_float(soup.find('main').find('ul').findAll('li')[1].get_text())
    href = soup.find('a', text='spectrum')
    if href is not None:  # check if contains download link
        try:  # check if contains resolution
            res = extract_float(soup.find('th', text='Resolution').find_next_sibling('td').get_text())
        except:
            res = None

        try:  # check if contains state
            state = soup.find('th', text='State').find_next_sibling('td').get_text().replace('\n', '')
            gas_bool = 'gas' in strip(state).lower()
        except:
            state = None
            gas_bool = False
        if name in valid.keys() and valid[name][5]:  # check if data already exists for gas
            return
        valid.update({name: [url, urljoin(parent, href.get('href')), mw, res, state, gas_bool]})
    elif name in valid.keys() or name in invalid.keys():  # check for dupe with existing data
        return
    else:
        try:  # check if data doesn't exist
            if strip(soup.find('h3').find_next(
                    'p').get_text()) == 'Adigitizedversionofthisspectrumisnotcurrentlyavailable.':
                unavailable.append(url)
                return
        except:
            pass
        invalid.update({name: [url, mw]})  # store other data to look at later

    time.sleep((time.time() - start))


def parse_search(lbound, stride, output=True):
    split = 10
    if output:
        print(f'processing M.W range [{round(float(lbound), 2)}, {round(float(lbound + stride), 2)}]')
    url = generate_mw_search(lbound, stride)
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    if strip(soup.findAll('h1')[-1].get_text()) == 'NoMatchingSpeciesFound':
        return
    elif strip(soup.findAll('h1')[-1].get_text()) != 'SearchResults':
        parse_page(url)
    elif strip(soup.find('main').find('p').get_text()) == 'Duetothelargenumberofmatchingspecies,' \
                                                          'onlythefirst400willbeshown.':
        for j in range(split):
            parse_search(lbound + j * (stride / split), stride / split)
    else:
        for link in soup.find('ol').find_all('a'):
            parse_page(urljoin(parent, link.get('href')))


"""
parse_search(0, 2000)

with open('Dataset/valid', 'wb') as file:
    pickle.dump(valid, file)
with open('Dataset/invalid', 'wb') as file:
    pickle.dump(invalid, file)
with open('Dataset/unavailable', 'wb') as file:
    pickle.dump(unavailable, file)
"""
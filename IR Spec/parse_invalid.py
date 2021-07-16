import pickle
import os
import time
from bs4 import BeautifulSoup
import requests
import nist_scrape as ns

with open('Dataset/invalid', 'rb') as file:
    invalid = pickle.load(file)


def generate_page(page_url, index):
    return f'{page_url}&Type=IR-SPEC&Index={index}#IR-SPEC'


def parse_invalid(url):
    start = time.time()

    soup = BeautifulSoup(requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT '
                                                                  '10.0; Win64; x64) '
                                                                  'AppleWebKit/537.36 (KHTML, '
                                                                  'like Gecko) '
                                                                  'Chrome/91.0.4472.106 '
                                                                  'Safari/537.36'}).content, 'html.parser')
    name = soup.findAll('h1')[-1].get_text()
    mw = ns.extract_float(soup.find('main').find('ul').findAll('li')[1].get_text())
    href = soup.find('a', text='spectrum')



"""
for key in invalid.keys():
    print(invalid[key][0])
"""




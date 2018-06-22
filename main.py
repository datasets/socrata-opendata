import csv
import json
import os
import shutil
import urllib
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup
from datapackage import Package


url = 'https://opendata.socrata.com/browse?'
raw_data_url = 'https://opendata.socrata.com/api/views'
category = ''


def init(file='generated_links.txt'):
    links_empty = False
    with open(file, "r") as links:
        if len(links.readlines()) == 0:
           links_empty = True

    if links_empty:
        generate_links()

    with open(file, "r") as links:
        for i, link in enumerate(links.readlines()):
            link = link.strip()
            print(str(i) + ': ' + str(link))
            try:
                generate_dataset(link)
            except HTTPError:
                print('Error occured')


def generate_dataset(url):
    global category
    if 'Category' in url:
        category = url.split(':')[1]
        return

    csv_url = raw_data_url + url[url.rindex('/'):] + '/rows.csv?accessType=DOWNLOAD'

    rows = []

    title = url[len('https://opendata.socrata.com/'+category+'/'): url.rindex('/')].lower()
    directory = "datasets/" + category + '/' + title
    if not os.path.exists(directory + "/data/"):
        os.makedirs(directory + "/data/")
    with open(directory + "/data/" + title + '.csv', "w", encoding='utf-8') as output_file:
        number_of_values = 0
        for i, line in enumerate(urlopen(csv_url)):
            decoded_line = line.decode('ascii', 'ignore')
            decoded_line = decoded_line.replace('\n', '')
            decoded_line = decoded_line.replace('\t', '')
            value_list = decoded_line.split(',')
            if i == 0:
                number_of_values = len(value_list)

            if len(value_list) != number_of_values:
                continue

            if all(value is "" for value in value_list):
                continue

            decoded_line = decoded_line.strip().lower()
            decoded_line = decoded_line.replace('"', '')
            if decoded_line not in rows:
                output_file.write(decoded_line + '\n')
                rows.append(decoded_line)

    number_of_rows = 0
    with open(directory + "/data/" + title + '.csv', "r", encoding='utf-8') as output_file:
        reader = csv.DictReader(output_file)
        for row in reader:
            number_of_rows += 1

    if number_of_rows < 50:
        shutil.rmtree(directory)
        return

    data_valid = datapackage_creator(location="datasets/" + category + '/' + title,
                                     title=title.title().replace('-', ' '),
                                     name=title,
                                     source_title='FiveThirtyEight - ' + title.title().replace('-', ' '),
                                     source_path=url)

    if not data_valid:
        shutil.rmtree(directory)
        return

    soup = BeautifulSoup(urlopen(url), 'html.parser')
    for meta in soup.find_all('meta'):
        meta_name = meta.get('name')
        if meta_name and 'description' in meta_name:
            with open(directory + '/README.md', "w", encoding='utf-8') as output_file:
                output_file.write('## ' + title.title().replace('-', ' ') + '\n')
                decoded_line = meta.get('content').strip().replace('"', '')
                output_file.write(decoded_line + '\n')

                output_file.write("\nThis dataset was scraped from [Socrata - " + title + '](' + url + ')')


def datapackage_creator(location, title, name, source_title, source_path):
    package = Package()

    package.descriptor['title'] = title
    package.descriptor['name'] = name

    package.descriptor['sources'] = [{}]
    package.descriptor['sources'][0]['title'] = source_title
    package.descriptor['sources'][0]['path'] = source_path

    package.descriptor['licences'] = [{}]
    package.descriptor['licences'][0]['name'] = 'odc-pddl'
    package.descriptor['licences'][0]['title'] = 'Open Data Commons Public Domain Dedication and Licence (PDDL)'
    package.descriptor['licences'][0]['path'] = 'http://opendatacommons.org/licenses/pddl/'

    package.commit()
    package.infer(location + '/data/*.csv')
    package_json = package.descriptor
    del package_json['profile']

    for resource in package_json['resources']:
        resource['path'] = resource['path'][len(location) + 1:]

    if package.valid:
        with open(location + '/datapackage.json', 'w') as data_file:
            json.dump(package_json, data_file, indent=4, sort_keys=True)
        return True
    else:
        print('DATAPACKAGE IS NOT VALID')
        return False


def generate_links():
    open('generated_links.txt', "w", encoding='ascii')
    categories = ['Business', 'Demo', 'Education', 'Fun', 'Government', 'Personal', 'Public+Safety']
    for category in categories:
        print(category)
        with open('generated_links.txt', "a") as generated_links:
            generated_links.write('Category:' + category + '\n')
        for i in range(10):
            soup = BeautifulSoup(urlopen(url + 'category=' + category + '&limitTo=datasets&page=' + str(i+1)), 'html.parser')
            with open('generated_links.txt', "a", encoding='ascii') as generated_links:
                for a in soup.find_all('a'):
                    clazz = a.get('class')
                    if a and clazz and 'browse2-result-name-link' in clazz:
                        href = a.get('href')
                        try:
                            generated_links.write(href + '\n')
                            print(href)
                        except UnicodeEncodeError:
                            print('Error: ' + href)
                            continue


init()

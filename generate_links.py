from bs4 import BeautifulSoup
from urllib.request import urlopen

url = 'https://opendata.socrata.com/browse?'


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


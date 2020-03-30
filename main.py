import hashlib
import requests


class Iterator():
    def __init__(self):
        self.url = 'https://raw.githubusercontent.com/mledoze/countries/master/countries.json'
        self.response = requests.get(self.url).json()
        self.index = -1
        self.end = len(self.response)

    def __iter__(self):
        return self

    def __next__(self):
        if self.end - 1 == self.index:
            raise StopIteration
        self.index += 1
        country = self.response[ self.index ]
        country_name = country[ 'name' ]
        official_name = country_name[ 'official' ]
        link = f'https://en.wikipedia.org/wiki/{official_name}'
        link = link.replace(" ", "_")
        return f'{official_name} - {link}'


def gen():
    with open('countries.txt') as f:
        for line in f:
            line = line.strip()
            link_for_hash = line.encode()
            h = hashlib.md5(link_for_hash).hexdigest()
            yield {line: h}

if __name__ == '__main__':
    iterator = Iterator()
    d = dict()
    with open('countries.txt', 'w', encoding='utf-8') as f:
        for i in iterator:
            f.writelines(i + '\n')
    for country in gen():
        print(country)

from bs4 import BeautifulSoup
import requests, random, re

USER_AGENT_LIST = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
)

class Citilink:
    def __init__(self):
        self.class_product_price = ('ProductHeader__price-default_current-price js--ProductHeader__price-default_current-price',)
        self.class_product_name = 'Heading Heading_level_1 ProductHeader__title'

    def get_product_info(self, url):
        if type(url) is str:
            link = url.strip().replace('/www.', '/')
            find_res = re.findall('https://([\w\-]+.[\w]+)', link)
            if not find_res:
                return -1
            elif find_res[0] not in SUPPORTED_SITES:
                return -1
        else:
            return -2

        client_headers = {
            'User-Agent': random.choice(USER_AGENT_LIST)
        }

        try:
            connection = requests.get(url, headers=client_headers)
            if connection.status_code != 200:
                print('Status code %s: %d' % (url, connection.status_code))
                return -3

        except requests.exceptions.ConnectionError:
            return -4
        
        return self.get_product_name_price(connection)

    def get_product_name_price(self, connection):
        site_content = connection.text
        soup = BeautifulSoup(site_content, 'lxml')
        price = ''

        for class_name in self.class_product_price:
            try:
                price = soup.find_all('span', class_=class_name)[0].text.strip()
                price = ''.join(re.findall('\d+', price))
                break
            except IndexError:
                continue

        if not price:
            price = '-1'

        try:
            name = soup.find_all('h1', class_=self.class_product_name)[0].text.strip()
        except IndexError:
            name = 'Error'

        return (name, price)

class Ozon(Citilink):
    def __init__(self):
        super()
        self.class_product_price = ('rj7 r7j', 'rj7 jr8', 'kr8 k8r', 'kr8')
        self.class_product_name = 'tk'

SHOPS_OBJECTS_DICTIONARY = {
        'citilink.ru': Citilink,
        'ozon.ru': Ozon
}
SUPPORTED_SITES = tuple(SHOPS_OBJECTS_DICTIONARY.keys())

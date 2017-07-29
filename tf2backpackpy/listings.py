import login
import requests

class Listings:

    GET_TOKEN = "https://backpack.tf/api/aux/token/v1?"
    REMOVE_LISTING = "https://backpack.tf/classifieds/remove/"
    SELL_LISTING = "https://backpack.tf/classifieds/sell/"

    def __init__(self, username, password, shared_secret, apikey=''):
        self._session = login.Login(username, password, shared_secret)
        self._session.start_backpack_session()
        self._session = self._session.getInfo()
        self.apikey = apikey
        if apikey:
            r = requests.get(Listings.GET_TOKEN,{'key':self.apikey}).json()
            if "message" in r.keys():
                raise Exception(r['message'])
            self.token = r['token']

    @property
    def cookies(self):
        cookies = {
            'PHPSESSID': self._session.cookies['PHPSESSID'],
            'stack[hash]': self._session.cookies['stack[hash]'],
            'stack[user]': self._session.cookies['stack[user]'],
            'user-id': self._session.cookies['user-id']
        }
        return cookies

    @staticmethod
    def gen_headers(path, ref):
        headers = {
            'authority': 'backpack.tf',
            'method': 'POST',
            'path': path,
            'scheme': 'https',
            'origin': 'https://backpack.tf',
            'referer': ref,
            'user-agent': 'python-requests/2.18.1',
            'accept-encoding': 'identity, deflate, compress, gzip',
            'accept-language': 'en-US,en;q=0.8'
        }
        return headers

    def remove_listing(self, appid:str, assetid:str, steamid:str):

        url = Listings.REMOVE_LISTING + appid+'_'+assetid
        headers = Listings.gen_headers(f'/classifieds/remove/{assetid}',
                                   f'https://backpack.tf/classifieds?steamid={steamid}')
        r = requests.Request('POST', url, headers=headers, cookies=self.cookies,
                             data={'user-id':self.cookies['user-id']})
        prepped = r.prepare()
        return self._session.send(prepped)

    def create_sell_listing(self, assetid, metal, keys, tradeoffer_url, offers=1, buyout=0, details=''):

        url = Listings.SELL_LISTING + assetid
        headers = Listings.gen_headers(f'/classifieds/sell/{assetid}', url)
        data = {
            "user-id":self.cookies['user-id'],
            "currencies[metal]":metal,
            "currencies[keys]":keys,
            "details":details,
            "offers":offers,
            "buyout":buyout,
            "tradeoffers_url":tradeoffer_url
        }
        r = requests.Request('POST', url, headers=headers, cookies=self.cookies, data=data)
        prepped = r.prepare()
        return self._session.send(prepped)

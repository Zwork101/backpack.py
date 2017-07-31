import login
import requests
from urllib import parse

class Listings:

    GET_TOKEN = "https://backpack.tf/api/aux/token/v1?"
    REMOVE_LISTING = "https://backpack.tf/classifieds/remove/"
    SELL_LISTING = "https://backpack.tf/classifieds/sell/"
    GET_MY_LISTINGS = "https://backpack.tf/api/classifieds/listings/v1"
    GET_LISTINGS = "https://backpack.tf/api/classifieds/search/v1"
    BUY_LISTING = "https://backpack.tf/classifieds/buy/"

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

    def _supply_data(self, metal, keys, details, offers, buyout, tradeoffer_url):
        data = {
            "user-id": self.cookies['user-id'],
            "currencies[metal]": metal,
            "currencies[keys]": keys,
            "details": details,
            "offers": offers,
            "buyout": buyout,
            "tradeoffers_url": tradeoffer_url
        }
        return data

    def remove_sell_listing(self, appid:str, assetid:str, steamid:str):
        url = Listings.REMOVE_LISTING + appid+'_'+assetid
        headers = Listings.gen_headers(f'/classifieds/remove/{assetid}',
                                   f'https://backpack.tf/classifieds?steamid={steamid}')
        r = requests.Request('POST', url, headers=headers, cookies=self.cookies,
                             data={'user-id':self.cookies['user-id']})
        prepped = r.prepare()
        return self._session.send(prepped)

    def remove_buy_listing(self, appid:str, steamid:str, obj_id:str):
        id = f'{appid}_{steamid}_{obj_id}'
        headers = Listings.gen_headers(f'/classifieds/remove/{id}',
                                       f'https://backpack.tf/classifieds?steamid={steamid}')
        r = requests.Request('POST', Listings.REMOVE_LISTING + id, headers=headers, cookies=self.cookies,
                             data={'user-id': self.cookies['user-id']})
        prepped = r.prepare()
        return self._session.send(prepped)

    def create_sell_listing(self, assetid, metal, keys, tradeoffer_url, offers=1, buyout=0, details=''):
        url = Listings.SELL_LISTING + assetid
        headers = Listings.gen_headers(f'/classifieds/sell/{assetid}', url)
        data = self._supply_data(metal, keys, details, offers, buyout, tradeoffer_url)
        r = requests.Request('POST', url, headers=headers, cookies=self.cookies, data=data)
        prepped = r.prepare()
        return self._session.send(prepped)

    def create_buy_listing(self, type, item, tradeoffers_url, metal, keys, craftable=True, offers=1, buyout=0, details=''):
        data = self._supply_data(metal, keys, details, offers, buyout, tradeoffers_url)
        url = f'{type}/{parse.quote(item)}/Tradable/'
        if craftable:
            url += 'Craftable'
        else:
            url += 'Non-Craftable'
        headers = Listings.gen_headers(url, Listings.BUY_LISTING + url)
        r = requests.Request('POST', Listings.BUY_LISTING + url, headers=headers, cookies=self.cookies, data=data)
        prepped = r.prepare()
        return self._session.send(prepped)

    def get_my_listings(self, item_names=0, intent:int=None, inactive=1):
        if not self.apikey:
            raise ValueError('apikey not supplied')
        payload = {'item_names':item_names, 'inactive':inactive, 'token':self.token}
        if intent:
            payload['intent'] = intent
        r = requests.get(Listings.GET_MY_LISTINGS, payload).json()
        if 'message' in r.keys():
            raise Exception(r['message'])
        return r

    def search_listings(self, item, item_names=0, intent:('dual', 'buy', 'sell')='dual', page_size=10, fold=1, steamid=None, **kwargs):
        if not self.apikey:
            raise ValueError('apikey not supplied')
        payload = {'item':item, 'item_names':item_names, 'intent':intent, 'page_size':page_size, 'fold':fold, 'key':self.apikey}
        if steamid:
            payload['steamid'] = steamid
        payload.update(kwargs)
        r = requests.get(Listings.GET_LISTINGS, payload).json()
        return r

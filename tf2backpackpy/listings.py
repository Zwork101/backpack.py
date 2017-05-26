import requests
from tf2backpackpy.utils import *
from urllib.parse import quote

class Listings:

    GET_LISTINGS = "https://backpack.tf/api/classifieds/listings/v1?"
    POST_LISTINGS = "https://backpack.tf/api/classifieds/list/v1?"
    SEARCH_LISTINGS = "https://backpack.tf/api/classifieds/search/v1?"
    GET_TOKEN = "https://backpack.tf/api/aux/token/v1?"
    GET_KEY = "https://backpack.tf/api/aux/key/v1?"

    def __init__(self, APIkey='', Token=''):
        if Token == '' and APIkey == '':
            raise MustHaveAtleastOneParameter()
        if Token != '':
            self.token = Token
        if APIkey != '':
            self.key = APIkey

    def get_token(self):
        result = requests.get(Listings.GET_TOKEN,{'key':self.key})
        if "message" in result.json().keys():
            raise InvalidLogin(result.json()['message'])
        self.token = result.json()['token']
        return None

    def get_key(self):
        result = requests.get(Listings.GET_KEY,{'token':self.token})
        if "message" in result.json().keys():
            raise InvalidLogin(result.json()['message'])
        self.key = result.json()['key']['$oid']
        return None

    def get_listings(self, item_names=0, intent=1, inactive=0):
        get = requests.get(Listings.GET_LISTINGS, {'token':self.token,'item_names':item_names,'intent':intent,'inactive':inactive})
        if "message" in get.json().keys():
            raise RequestError(get.json()['message'])
        return get.json()

    def create_listing(self, intent, id, item : dict, offers=1, buyout=1, promoted=0, details='', **kwargs):
        item['quality'] = quote(item['quality'])
        item['item_name'] = quote(item['item_name'])
        payload = {'token':self.token, 'intent':intent, 'id':id, 'item':str(item), 'offers':offers, 'buyout':buyout, 'details':details}
        payload.update(kwargs)
        print(Listings.POST_LISTINGS + payload)
        post = requests.post(Listings.POST_LISTINGS,payload)
        if 'message' in post.json().keys():
            raise RequestError(post.json()['message'])
        return post.json()['listings']

    def search_listings(self, item, item_name=0, intent='dual', page_size=10, fold=1, steamid=None, **kwargs):
        item = quote(item)
        if steamid == None:
            payload = {'key' :self.key, 'item' :item, 'item_name' :item_name, 'intent' :intent, 'page_size' :page_size,\
                       'fold':fold}
        else:
            payload = {'key': self.key, 'item': item, 'item_name': item_name, 'intent': intent, 'page_size': page_size,\
                       'fold': fold, 'steamid':steamid}
        payload.update(kwargs)
        get = requests.get(Listings.SEARCH_LISTINGS,payload)
        if "message" in get.json().keys():
            raise RequestError(get.json()['message'])
        return get.json()

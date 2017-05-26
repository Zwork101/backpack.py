from urllib.parse import quote
import requests
from tf2backpackpy.utils import *


class Pricer:

    GET_TOKEN = "https://backpack.tf/api/aux/token/v1?"
    GET_KEY = "https://backpack.tf/api/aux/key/v1?"
    GET_CLASSIFIEDS = "https://backpack.tf/api/IGetPrices/v4?"
    GET_HISTORY = "https://backpack.tf/api/IGetPriceHistory/v1?"
    GET_CURRENCIES = "https://backpack.tf/api/IGetCurrencies/v1?"
    GET_SPECIAL_ITEMS = "http://backpack.tf/api/IGetSpecialItems/v1?"

    def __init__(self, APIkey=None, Token=None):
        if Token == '' and APIkey == '':
            raise MustHaveAtleastOneParameter()
        if Token != '':
            self.token = Token
        if APIkey != '':
            self.key = APIkey

    def get_token(self):
        result = requests.get(Pricer.GET_TOKEN,{'key':self.key})
        if "message" in result.json().keys():
            raise InvalidLogin(result.json()['message'])
        self.token = result.json()['token']
        return None

    def get_key(self):
        result = requests.get(Pricer.GET_KEY,{'token':self.token})
        if "message" in result.json().keys():
            raise InvalidLogin(result.json()['message'])
        self.key = result.json()['key']['$oid']
        return None

    def get_classifieds(self, raw=None, since=None):
        if raw == None and since == None:
            get = requests.get(Pricer.GET_CLASSIFIEDS,{'key':self.key})
        if raw != None and since == None:
            get = requests.get(Pricer.GET_CLASSIFIEDS,{'key':self.key, 'raw':raw})
        if raw == None and since != None:
            get = requests.get(Pricer.GET_CLASSIFIEDS,{'key':self.key, 'since':since})
        if raw != None and since != None:
            get = requests.get(Pricer.GET_CLASSIFIEDS, {'key':self.key, 'raw':raw, 'since':since})
        gJson = get.json()['response']
        if gJson['success'] == 0:
            raise RequestError(gJson['message'])
        return gJson

    def get_history(self, item, quality, appid=440, tradeable=1, craftable=1):
        item = quote(item)
        quality = quote(quality)
        get = requests.get(Pricer.GET_HISTORY, {'key':self.key,'item':item,'quality':quality, \
                                                'appid':appid,'tradeable':tradeable,'craftable':craftable})
        gJson = get.json()['response']
        if gJson['success'] == 0:
            raise RequestError(gJson['message'])
        return gJson

    def get_currencies(self, raw=0):
        get = requests.get(Pricer.GET_CURRENCIES, {'key':self.key,'raw':raw})
        if get.json()['response']['success'] == 0:
            raise RequestError(get.json()['response']['message'])
        return get.json()['response']['currencies']

    def get_special_items(self, appid=440):
        get = requests.get(Pricer.GET_SPECIAL_ITEMS, {'key':self.key, 'appid':appid})
        if get.json()['response']['success'] == 0:
            raise RequestError(get.json()['response']['message'])
        return get.json()['response']['items']



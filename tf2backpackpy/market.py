from tf2backpackpy.utils import *
import requests

class Market:

    GET_MARKET_PRICE = "https://backpack.tf/api/IGetMarketPrices/v1?"
    MARKET_IMAGES = "https://backpack.tf/api/market/images/v1?"
    GET_TOKEN = "https://backpack.tf/api/aux/token/v1?"
    GET_KEY = "https://backpack.tf/api/aux/key/v1?"

    def __init__(self, APIkey=None, Token=None):
        if Token == '' and APIkey == '':
            raise MustHaveAtleastOneParameter()
        if Token != '':
            self.token = Token
        if APIkey != '':
            self.key = APIkey

    def get_token(self):
        result = requests.get(Market.GET_TOKEN,{'key':self.key})
        if "message" in result.json().keys():
            raise InvalidLogin(result.json()['message'])
        self.token = result.json()['token']
        return None

    def get_key(self):
        result = requests.get(Market.GET_KEY,{'token':self.token})
        if "message" in result.json().keys():
            raise InvalidLogin(result.json()['message'])
        self.key = result.json()['key']['$oid']
        return None

    def get_market_price(self, appid=440):
        get = requests.get(Market.GET_MARKET_PRICE, {'key':self.key,'appid':appid})
        gJson = get.json()['response']
        if gJson['success'] == 0:
            raise RequestError(gJson['message'])
        return gJson['items']

    def get_market_images(self):
        get = requests.get(Market.MARKET_IMAGES, {'key':self.key})
        if "message" in get.json().keys():
            raise RequestError(get.json()['message'])
        return get.json()
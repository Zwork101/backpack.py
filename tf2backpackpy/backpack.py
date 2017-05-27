from tf2backpackpy.utils import *
import json
from urllib.parse import quote

class Backpack:

    GET_TOKEN = "https://backpack.tf/api/aux/token/v1?"
    GET_KEY = "https://backpack.tf/api/aux/key/v1?"
    HEARTBEAT = "https://backpack.tf/api/aux/heartbeat/v1?"
    SUBSCRIPTIONS = "https://backpack.tf/api/subscriptions/prices/v1?"
    LISTING_SUBSCRIPTIONS = "https://backpack.tf/api/subscriptions/listings/v1?"

    def __init__(self, APIkey='', Token=''):
        if Token == '' and APIkey == '':
            raise MustHaveAtleastOneParameter()
        if Token != '':
            self.token = Token
        if APIkey != '':
            self.key = APIkey

    def get_token(self):
        result = requests.get(Backpack.GET_TOKEN,{'key':self.key})
        if "message" in result.json().keys():
            raise InvalidLogin(result.json()['message'])
        self.token = result.json()['token']
        return None

    def get_key(self):
        result = requests.get(Backpack.GET_KEY,{'token':self.token})
        if "message" in result.json().keys():
            raise InvalidLogin(result.json()['message'])
        self.key = result.json()['key']['$oid']
        return None

    def beat(self,automatic : str):
        put = requests.post(Backpack.HEARTBEAT,{'token':self.token,'automatic':automatic})
        if 'message' in put.json().keys():
            raise RequestError(put.json()['message'])
        return put.json()['bumped']

    def subscriptions(self):
        result = requests.get(Backpack.SUBSCRIPTIONS,{'token':self.token})
        if 'message' in result.json().keys():
            raise RequestError(result.json()['message'])
        return result.json()["subscriptions"]

    def create_subscription(self,item_name):
        item_name = quote(item_name)
        print(item_name)
        put = requests.put(Backpack.SUBSCRIPTIONS,{'token':self.token,'item_name':item_name})
        try:
            if 'message' in put.json().keys():
                raise RequestError(put.json()['message'])
        except json.decoder.JSONDecodeError:
            return put.content.decode()

    def remove_subscription(self,item_name):
        item_name = quote(item_name)
        print(item_name)
        deleted = requests.delete(Backpack.SUBSCRIPTIONS + f'token={self.token}&item_name={item_name}')
        try:
            if 'message' in deleted.json().keys():
                raise RequestError(deleted.json()['message'])
        except json.decoder.JSONDecodeError:
            return deleted.content.decode()

    def listing_subscriptions(self):
        get = requests.get(Backpack.LISTING_SUBSCRIPTIONS,{'token':self.token})
        if 'message' in get.json().keys():
            raise RequestError(get.json()['message'])
        return get.json()["subscriptions"]

        def create_listings_subscription(self,item_name,intent,blanket=0,currency=0,min=0,max=0):
        item_name = quote(item_name)
        if blanket == 0 and currency == 0:
            raise MustHaveAtleastOneParameter()
        if blanket != 0 and currency != 0:
            raise MustHaveAtleastOneParameter()
        else:
            put = requests.put(Backpack.LISTING_SUBSCRIPTIONS,{'token':self.token,'intent':intent,'blanket':blanket, \
                               'min':min,'max':max, 'currency':currency})
            try:
                if 'message' in put.json().keys():
                    raise RequestError(put.json()['message'])
                return put.content.decode()
            except json.decoder.JSONDecodeError:
                RequestError("listing was not created")

    def delete_listing_subscription(self, item_name, intent):
        item_name = quote(item_name)
        print(Backpack.SUBSCRIPTIONS + f'token={self.token}&item_name={item_name}&intent={intent}')
        deleted = requests.delete(Backpack.SUBSCRIPTIONS + f'token={self.token}&item_name={item_name}&intent={intent}')
        try:
            if 'message' in deleted.json().keys():
                raise RequestError(deleted.json()['message'])
        except json.decoder.JSONDecodeError:
            return deleted.content.decode()

from urllib import parse

import requests

from backpackpy import login


class Notifications:

    GET_TOKEN = "https://backpack.tf/api/aux/token/v1?"
    ITEM_ALERT = "https://backpack.tf/classifieds/subscriptions/"

    def __init__(self, username, password, shared_secret, apikey=''):
        self._session = login.Login(username, password, shared_secret)
        self._session.start_backpack_session()
        self._session = self._session.getInfo()
        self.apikey = apikey
        if apikey:
            r = requests.get(Notifications.GET_TOKEN,{'key':self.apikey}).json()
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
    def gen_headers(path, ref, method):
        headers = {
            'authority': 'backpack.tf',
            'method': method,
            'path': path,
            'scheme': 'https',
            'origin': 'https://backpack.tf',
            'referer': ref,
            'user-agent': 'python-requests/2.18.1',
            'accept-encoding': 'identity, deflate, compress, gzip',
            'accept-language': 'en-US,en;q=0.8'
        }
        return headers

    def remove_listing_alert(self, intent, item_name):
        data = {
            "user-id": self.cookies['user-id'],
            "intent":intent,
            "item_name":item_name
        }
        headers = Notifications.gen_headers("/classifieds/subscriptions", "https://backpack.tf/subscriptions", "DELETE")

        r = requests.Request('DELETE', Notifications.ITEM_ALERT, data=data,
                             cookies=self.cookies, headers=headers)
        prepped = r.prepare()
        return self._session.send(prepped)

    def add_listing_alert(self, intent, type, item_raw_name, blanket=1, craftable=True):
        url = Notifications.ITEM_ALERT+ type +'/'+ parse.quote(item_raw_name) + '/Tradable/'
        data = {
            "user-id": self.cookies['user-id'],
            "item_name":type + ' ' + item_raw_name,
            "intent":intent,
            "blanket":blanket
        }
        if craftable:
            url += 'Craftable'
        else:
            url += 'Non-Craftable'
        headers = Notifications.gen_headers('/classifieds/subscriptions', url, 'PUT')
        r = requests.Request('PUT', Notifications.ITEM_ALERT, data=data, headers=headers, cookies=self.cookies)
        prepped = r.prepare()
        return self._session.send(prepped)


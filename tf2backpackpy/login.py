import base64
import time
import rsa
import requests
from guard import SteamGuard

class Login(object):
    def __init__(self, username, password, shared_secret):
        self.session = requests.session()
        self.resp = requests.post("https://store.steampowered.com" + "/login/getrsakey/", data={
            "username": str(username),
        }).json()
        self.rsa_modulus = self.rsa_params(str(username)).get('rsa_mod')
        self.rsa_exponent = self.rsa_params(str(username)).get('rsa_exp')
        self.rsa_timestamp = self.rsa_params(str(username)).get('rsa_timestamp')
        self.rsa_publickey = rsa.PublicKey(self.rsa_modulus, self.rsa_exponent)
        self.encrypted_password = base64.b64encode(rsa.encrypt(str(password).encode('UTF-8'), self.rsa_publickey))
        self.steamguard = SteamGuard()
        self.loginReq = self.loginRequest(str(username), str(self.encrypted_password), str(shared_secret))

    def rsa_params(self, username):
        requests.post("https://store.steampowered.com" + "/login/getrsakey/", data={
            "username": str(username),
        })
        return dict({'rsa_mod': int(self.resp['publickey_mod'], 16),
                     'rsa_exp': int(self.resp['publickey_exp'], 16),
                     'rsa_timestamp': int(self.resp['timestamp']),
                     })

    def loginRequest(self, username, encrypted_password, shared_secret):
        loginForm = dict({
            "password": str(encrypted_password),
            "username": str(username),
            "twofactorcode": self.steamguard.get_confirmation_key(time.time(), str(shared_secret)),
            "emailauth": "",
            "loginfriendlyname": "",
            "captchagid": "-1",
            "captcha_text": "",
            "emailsteamid": "",
            "rsatimestamp": str(self.rsa_params(str(username)).get('rsa_timestamp')),
            "remember_login": "false",
            "donotcache": str(int(time.time()) * 1000)
        })
        login_request = self.session.post("https://store.steampowered.com" + "/login/dologin", data=loginForm)
        loginreq_dict = login_request.json()
        transfer_parameters = loginreq_dict.get('transfer_parameters')
        if transfer_parameters is None:
            raise Exception("No transfer parameters have been fetched") # Most likely raised because of authentication failure
        for url in loginreq_dict['transfer_urls']:
            self.session.post(url, transfer_parameters)
        sessionid = self.session.cookies.get_dict()['sessionid']
        community_domain = "steamcommunity.com"
        store_domain = "store.steampowered.com"
        community_cookie = {"name": "sessionid",
                            "value": str(sessionid),
                            "domain": str(community_domain)}
        store_cookie = {"name": "sessionid",
                        "value": str(sessionid),
                        "domain": str(store_domain)}
        self.session.cookies.set(**community_cookie)
        self.session.cookies.set(**store_cookie)
        return self.session

    def getInfo(self): # Return Requests Login Session
        return self.loginReq


import requests
import time
import rsa
import base64

class BaseLogin:
    def __init__(self, username:str, password:str, auth_code:str=None, verify:bool=True):
        """
        __init__ for login data
        :param username:
        :param password:
        :param auth_code:
        :param verify:
        """
        self.name = username
        self.pw = password
        self.auth = auth_code
        self.session = requests.Session()
        self.verify = verify

    def _getsession(self):
        g = self.session.get('http://backpack.tf', verify=self.verify)
        p = self.session.post('http://backpack.tf/login', allow_redirects=True, verify=self.verify)

    def _getrsa(self):
        payload = {'donotcache':BaseLogin.get_time_stamp(), 'username':self.name}
        key = self.session.post('https://store.steampowered.com/login/getrsakey', data=payload, verify=self.verify)
        if key.json()['success'] == True:
            key = key.json()
            self.tm = key['timestamp']
            self.pkmd = int(key['publickey_mod'], 16)
            self.pkep = int(key['publickey_exp'], 16)
        else:
            raise ConnectionError('Could not obtain RSA key')
    def _dologin(self):
        if self.auth == None:
            payload = {'username':self.name, 'rsatimestamp':self.tm, 'donotcache':BaseLogin.get_time_stamp(),
                       'captcha_text':'', 'emailsteamid':'', 'emailauth':'', 'loginfriendlyname':'', 'captchagid':-1,
                       'remember_login':'false'}
        else:
            payload = {'username': self.name, 'rsatimestamp': self.tm, 'donotcache': BaseLogin.get_time_stamp(),
                       'captcha_text': '', 'emailsteamid': '', 'emailauth': '', 'loginfriendlyname': '',
                       'captchagid': -1, 'twofactorcode':self.auth, 'remember_login':'false'}
        rsa_key = rsa.PublicKey(self.pkmd, self.pkep)
        enc_pass = base64.b64encode(rsa.encrypt(self.pw.encode('utf-8'), rsa_key))
        payload['password'] = enc_pass
        r = self.session.post('http://store.steampowered.com/login/dologin', data=payload, verify=self.verify)
        if r.json()['success'] == False:
            print(r.status_code)
            print(r.content)
            r = r.json()
            if 'requires_twofactor' in r.keys():
                raise ConnectionError(r['message'])
            else:
                raise NameError('A twofactorcode is required')
        else:
            self.tran_par = r.json()['transfer_parameters']

    def _transfer_store(self):
        payload = {'donotcache':BaseLogin.get_time_stamp(), 'token':self.tran_par['token'], 'auth':self.tran_par['auth'],
                   'remember_login':False, 'webcookie':self.tran_par['webcookie'],
                   'token_secure':self.tran_par['token_secure']}
        self.session.post('http://store.steampowered.com/login/transfer', data=payload)
    def _transfer_help(self):
        payload = {'donotcache':BaseLogin.get_time_stamp(), 'token':self.tran_par['token'], 'auth':self.tran_par['auth'],
                   'remember_login':False, 'webcookie':self.tran_par['webcookie'],
                   'token_secure':self.tran_par['token_secure']}
        self.session.post('http://help.steampowered.com/login/transfer', data=payload)

    def _finnal_redirect(self):
        self.session.post('http://steamcommunity.com/openid/login', allow_redirects=True)

    def login(self):
        """
        Automate login through backpack.tf (Calls functions)
        :return None:
        """
        self._getsession()
        self._getrsa()
        self._dologin()
        self._transfer_store()
        self._transfer_help()
        self._finnal_redirect()

    def get_session(self):
        """
        Gives session required for backpack.tf
        :return request.Session():
        """
        return self.session

    @staticmethod
    def get_time_stamp():
        return str(int(time.time() * 1000))

if __name__ == '__main__':
    code = input('one_time_code: ')
    log = BaseLogin('Zwork101', 'pass', code)
    log.login()
    log.get_session()

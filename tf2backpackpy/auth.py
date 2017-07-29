from SteamLoginPy.authentication.login import Login
from bs4 import BeautifulSoup

class BackpackTfSession(object):
    def __init__(self, username, password, shared_secret):
        self.loginSession = (Login(str(username), str(password), str(shared_secret))).getInfo()
        self.openid_response = self.loginSession.post("https://backpack.tf/login")
        self.response_html = self.openid_response.text
        self.parameters = self.returnParameters(self.response_html)
        self.auth_resp = self.loginSession.post(self.openid_response.url, data=self.parameters)

    def session(self):
        return self.loginSession

    @staticmethod
    def returnParameters(html):
        soup = BeautifulSoup(html, "lxml")
        action = soup.findAll("input", {"name": "action"})[0]['value']  # Or "steam_openid_login" in most of the cases
        mode = soup.findAll("input", {"name": "openid.mode"})[0]['value']  # Or "checkid_setup" in most of the cases
        openidparams = soup.findAll("input", {"name": "openidparams"})[0]['value']
        nonce = soup.findAll("input", {"name": "nonce"})[0]['value']
        return {
            "action": action,
            "openid.mode": mode,
            "openidparams": openidparams,
            "nonce": nonce
        }



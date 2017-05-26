import requests

GET_USER = "https://backpack.tf/api/users/info/v1?key="

def get_user(key : str, Steam64IDS : tuple):
    ids = ''
    for id in Steam64IDS:
        if Steam64IDS[len(Steam64IDS) - 1] == id:
            ids += id
        else:
            ids += str(id) + ','
    request = GET_USER + key + '&steamids=' + ids
    get = requests.get(request)
    if "message" in get.json().keys():
        raise RequestError(get.json()['message'])
    return get.json()['users']

class MustHaveAtleastOneParameter(Exception):
    def __init__(self):
        Exception.__init__(self, "No paramenters, or too many, were supplied (Must have 1)")

class InvalidLogin(Exception):
    def __init__(self,*args):
        Exception.__init__(self, str(args))

class RequestError(Exception):
    def __init__(self, *args):
        Exception.__init__(self, str(args))

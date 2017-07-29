import time
from binascii import unhexlify
import requests
import hmac
import base64
import hashlib

class SteamGuard(object):
    def long_to_bytes(self, val, endianness='big'):
        width = 64
        fmt = '%%0%dx' % (width // 4)  # Format to number to bytes
        s = unhexlify(fmt % val)  # Binary data from hexadecimal number
        if (endianness == 'little'):  # In most cases, This boolean operation is not significant.
            s = s[::-1]
        return s

    def get_server_time(self):
        r = requests.post('https://api.steampowered.com:443/ITwoFactorService/QueryTime/v0001')
        jsn = r.json()
        return jsn.get('response').get('server_time')

    def get_confirmation_key(self, tm, secret):
        STEAM_CHARS = ['2',  # Official Steam characters, Works with ValveMobileApp
                       '3',
                       '4',
                       '5',
                       '6',
                       '7',
                       '8',
                       '9',
                       'B',
                       'C',
                       'D',
                       'F',
                       'G',
                       'H',
                       'J',
                       'K',
                       'M',
                       'N',
                       'P',
                       'Q',
                       'R',
                       'T',
                       'V',
                       'W',
                       'X',
                       'Y']

        def toLong(x): return long(x.encode('hex'), 16)  # Hexlify integer and convert it to long as hexadecimal (radix 16)

        def local(): return long(round(time.mktime(time.localtime(time.time())) * 1000))  # Exact time converted to seconds

        timediff = local() - (long(self.get_server_time()) * 1000)  # Time difference between steam server and machine

        def codeinterval(): return long((local() + timediff) / 30000)  # Code interval between steam server and machine

        v = self.long_to_bytes(val=codeinterval())  # Convert long integer to bytes

        h = hmac.new(base64.b64decode(secret), v, hashlib.sha1)  # Decode shared secret and then create hmac for $v

        digest = h.digest()

        start = toLong(digest[19]) & 0x0f  # Bitwse <AND> operation between long hexadecimal number and 15 (0x0f)

        b = digest[start:start + 4]  # Unfiltered code

        fullcode = toLong(b) & 0x7fffffff  # Unfiltered full code as long integer

        CODE_LENGTH = 5

        code = ''
        for i in range(CODE_LENGTH):
            code += STEAM_CHARS[fullcode % len(STEAM_CHARS)]  # Filtering code with steam characters
            fullcode /= len(STEAM_CHARS)  # Filtered full code as long integer (Divided by 26)
        return code

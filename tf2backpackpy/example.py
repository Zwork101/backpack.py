from tf2backpackpy.utils import *
from tf2backpackpy import backpack, listings, market, pricing

APIKEY = 'API KEY'
p_backpacks = {}
item = 'Ham Shank'

P = pricing.Pricer(APIKEY)
M = market.Market(APIKEY)
B = backpack.Backpack(APIKEY)
L = listings.Listings(APIKEY)

listings = L.search_listings(item)
for user in listings['sell']['listings']:
    userID = user['steamid']
    user_info = get_user(APIKEY, (userID,))
    value = user_info[userID]['inventory']['440']['keys']
    p_backpacks[user_info[userID]['name']] = value

for k, v in p_backpacks.items():
    print(f"{k} is selling a {item}. There backpack is worth {v} in keys")




import requests
import asyncio
import aiohttp
import json
import pprint
from datetime import datetime
session = aiohttp.ClientSession()
url = "https://us.api.battle.net/wow/"
apikey = 'gcda8kcybzchh63gwx634q2kyt57q5mg'

async def isTier(itemID):
    async with session.get(url + "item/%d" % itemID,
            params = {"apikey": apikey}) as resp:
        if resp.status >= 400:
            raise RuntimeError("piece not found.")
        r = await resp.json()
        if "itemSet" in r:
            x = r["itemSet"]["id"]
            return x >= 1301 and x <= 1312
        return False

async def inGuild(name, realm):
    async with session.get(url + "character/" + realm + "/" + name,
            params = {"apikey": apikey, "fields": "guild", "locale": "en_US"}
            ) as resp:
        if resp.status >= 400:
            return False
        r = await resp.json()
        return ("level" in r and r["level"] == 110 and
                    "guild" in r and r["guild"]["name"] == "Unified")

async def getRealm(name):
    m = await inGuild(name, "Madoran")
    d = await inGuild(name, "Dawnbringer")
    if m and d:
        raise RuntimeError("Name clash NYI")
    if m:
        return "Madoran"
    if d:
        return "Dawnbringer"
    raise RuntimeError("Toon not found")

difficulties = {"raid-finder": "LFR",
                "raid-normal": "normal",
                "raid-heroic": "heroic",
                "raid-mythic": "mythic"}
async def getTierInfo(player, piece):
    if not piece in player:
        return None #Not wearing anything in that slot?
    p = player[piece]
    if not await isTier(p["id"]):
        return None
    return {"IL": p["itemLevel"], "from": difficulties[p["context"]]}

slots = ["head", "shoulder", "back", "chest", "hands", "legs"]

async def getTierPieces(name):
    realm = await getRealm(name)
    async with session.get(url + "character/"
            + realm + "/" + name,
            params = {"apikey": apikey, "fields": "items", "locale": "en_US"}
            ) as resp:
        items = (await resp.json())["items"]
        ans = {}
        for slot in slots:
            ans[slot] = await getTierInfo(items, slot)
        return ans

enchantables = ["back", "finger1", "finger2", "neck"]

async def missingEnch(name):
    realm = await getRealm(name)
    async with session.get(url + "character/"
            + realm + "/" + name,
            params = {"apikey": apikey, "fields": "items", "locale": "en_US"}
            ) as resp:
        items = (await resp.json())["items"]
        ans = []
        for slot in enchantables:
            if (slot not in items
                    or 'enchant' not in items[slot]["tooltipParams"]):
                ans.append(slot)
        return ans

async def missingGemsCount(name):
    realm = await getRealm(name)
    async with session.get(url + "character/"
            + realm + "/" + name,
            params = {"apikey": apikey, "fields": "audit", "locale": "en_US"}
            ) as resp:
        return (await resp.json())["audit"]["emptySockets"]

# loop = asyncio.get_event_loop()
# print(loop.run_until_complete(missingEnch("Nyxstus")))
# session.close()
# loop.close()

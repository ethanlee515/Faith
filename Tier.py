import Armory
import asyncio
import aiofiles
import json
import pprint
from misc import *

rec = eval(open("tierInfo.dat", "r").read())

async def save(fName = "tierInfo.dat"):
    async with aiofiles.open(fName, "w") as f:
        pp = pprint.PrettyPrinter(indent = 4)
        await f.write(pp.pformat(rec) + "\n")

# async def remakeRecord(rList = raiders, fName = "tierInfo.dat"):
#     #This code just got 100% more idiot-proof
#     async with aiofiles.open("oldInfo.dat", "w") as oldrec:
#         pp = pprint.PrettyPrinter(indent = 4)
#         oldrec.write(pp.pformat(tierInfo) + "\n")
#     tierInfo.clear()
#     for r in rList:
#         print("searching up " + r + "...")
#         try:
#             tierInfo[r] = await Armory.getTierPieces(r)
#         except RuntimeError:
#             print(r + " not found.")
#     await save(fName)

nickname = {"sawbones": "asawbones",
            "sawbone": "asawbones",
            "bone": "asawbones",
            "bones": "asawbones",
            "rose": "rosaree",
            "ezme": "ezmë",
            "opd": "opdhealer",
            "op": "opdhealer",
            "deadeye": "deadeyedaisy",
            "sharla": "sharlá",
            "danny": "yaois"}

# async def updateRecord():
#     for r in rList:
#         print("searching up " + r + "...")
#         try:
#             tierInfo[r] = await Armory.getTierPieces(r)
#         except RuntimeError:
#             print(r + " not found.")
#     await save(fName)

def overWrite(p1, p2):
    if p2 == None:
        return True
    dLvl = {"LFR": 1, "normal": 2, "heroic": 3, "mythic": 4}
    if dLvl[p1["from"]] > dLvl[p2["from"]]:
        return True
    if "IL" not in p1:
        return False
    if ("IL" in p1 and "IL" not in p2) or p1["IL"] > p2["IL"]:
        return True
    return False

async def addPlayer(pName):
    r = pName.lower()
    rec[r] = await Armory.getTierPieces(r) #this COULD error
    await save()

async def removePlayer(pName):
    r = pName.lower()
    del rec[r]
    await save()

async def XWonY(x, slot, item):
    x = nickname[x] if x in nickname else x
    p2 = rec[x][slot]
    if overWrite(item, p2):
        rec[x][slot] = item

async def nameWon(name, difficulty, slot, il = None):
    item = {'from': difficulty}
    if il != None:
        item["IL"] = il
    XWonY(name, slot, item)

def getName(nameIn):
    if nameIn == "":
        return None
    if nameIn in nickname:
        return nickname[nameIn]
    if nameIn in rec.keys():
        return nameIn
    for k in rec:
        if k.startswith(nameIn):
            return k
    return None

slotKeys = {
    "head": ["head", "helm"],
    "shoulder": ["shoulder"],
    "back": ["back", "cloak"],
    "chest": ["chest"],
    "hands": ["hand", "gauntlet", "gloves"],
    "legs": ["legs", "legging", "pants"]
}

def getSlot(m):
    m = m.lower()
    for k, v in slotKeys.items():
        for s in v:
            if s in m:
                return k
    return None

def pieceDesc(name, slot):
    p = rec[name][slot]
    if p == None:
        return "non-tier"
    info = p["from"]
    if "IL" in p:
        info += " %d" % p["IL"]
    return info

def extractPiece(m):
    m = m.lower()
    dLst = [("lfr", "LFR"),
        ("mythic", "mythic"),
        ("heroic", "heroic"),
        ("norm", "normal")]
    diff = None
    for (d0, d1) in dLst:
        if d0 in m:
            diff = d1
            break
    if diff == None:
        return None
    il = getNum(m)
    return {"from": diff, "IL": il} if il > 0 else {"from": diff}

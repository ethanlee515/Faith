import Armory
import asyncio
import aiofiles
import json
import pprint
from misc import *

currentRaid = None #REALLY should be None.
#Setting to heroic as a hack for missing functionality.

rec = eval(open("tierInfo.dat", "r").read())

undoHistory = []

async def save(fName = "tierInfo.dat"):
    async with aiofiles.open(fName, "w") as f:
        pp = pprint.PrettyPrinter(indent = 4)
        await f.write((pp.pformat(rec) + "\n"))

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

defaultIL = {"LFR": 885, "normal": 900, "heroic": 915, "mythic": 930}

def getIL(piece):
    if piece == None:
        return 0
    return piece["IL"] if "IL" in piece else defaultIL[piece["from"]]

def overWrite(p1, p2):
    if p2 == None:
        return True
    return getIL(p1) > getIL(p2)

async def addPlayer(pName):
    r = pName.lower()
    rec[r] = await Armory.getTierPieces(r) #this COULD error
    await save()

async def removePlayer(pName):
    r = pName.lower()
    del rec[r]
    await save()

def winIssues(name, slot, item):
    if not overWrite(item, rec[name][slot]):
        return "Already had " + pieceDesc(name, slot) + "."
    if (getIL(rec[name][slot]) >= defaultIL["normal"]):
        return "Replacing " + pieceDesc(name, slot) + "."
    tierCount = 0
    tfCount = 0
    for s in Armory.slots:
        if s != slot:
            if getIL(rec[name][s]) >= defaultIL["normal"]:
                tierCount += 1
                if rec[name][s]["from"] == "LFR":
                    tfCount += 1
    if tierCount >= 4:
        if tfCount == 0:
            return "Already had %d tier pieces." % tierCount
        else:
            return ("Already had %d tier pieces, "
                    "%d of which are TF'd from LFR."
                        % (tierCount, tfCount))
    return ""

async def award(names, slot, piece):
    actions = []
    for name in names:
        if overWrite(piece, rec[name][slot]):
            actions.append((name, slot, rec[name][slot], piece))
            rec[name][slot] = piece
    await save()
    undoHistory.append(actions)

async def forceOverwrite(name, slot, piece):
    oldpiece = rec[name][slot]
    undoHistory.append([(name, slot, oldpiece, piece)])
    rec[name][slot] = piece
    await save()
    return pToS(oldpiece)

async def undo():
    if len(undoHistory) == 0:
        return []
    undone = []
    lst = undoHistory.pop()
    for (name, slot, oldpiece, newpiece) in lst:
        rec[name][slot] = oldpiece
        undone.append(name.capitalize() + "'s " + pToS(newpiece) + " " + slot +
            " has been reverted back to " + pToS(oldpiece))
    await save()
    return undone

def getName(nameIn):
    if nameIn == "":
        return None
    nameIn = nameIn.lower()
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

def pToS(p):
    if p == None:
        return "non-tier"
    info = p["from"]
    if "IL" in p:
        info += " %d" % p["IL"]
    return info

def pieceDesc(name, slot):
    return pToS(rec[name][slot])

def extractPiece(m):
    m = m.lower()
    dLst = [("lfr", "LFR"),
        ("mythic", "mythic"),
        ("heroic", "heroic"),
        ("norm", "normal")]
    diff = currentRaid
    for (d0, d1) in dLst:
        if d0 in m:
            diff = d1
            break
    if diff == None:
        return None
    il = getNum(m)
    return {"from": diff, "IL": il} if il > 0 else {"from": diff}

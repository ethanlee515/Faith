import Armory
import asyncio
import aiofiles
import json
import pprint
from misc import *

currentRaid = None

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
            "daisy": "deadeyedaisy",
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
    return getIL(p1) >= getIL(p2)

async def addPlayer(pName):
    r = pName.lower()
    if r in rec:
        raise RuntimeError
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

def winStr(name, slot, piece):
    issues = winIssues(name, slot, piece)
    s = name.capitalize() + " won " + pToS(piece) + " " + slot + "."
    if issues:
        s += " " + issues
    return s

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

def revertStr(name, slot, oldpiece, newpiece):
    return (name.capitalize() + "'s " + pToS(newpiece) + " " + slot +
            " has been reverted back to " + pToS(oldpiece))

async def undo():
    if len(undoHistory) == 0:
        return []
    undone = []
    lst = undoHistory.pop()
    for (name, slot, oldpiece, newpiece) in lst:
        rec[name][slot] = oldpiece
        undone.append(revertStr(name, slot, oldpiece, newpiece))
    await save()
    return undone

def searchHistory(name):
    for i in range(len(undoHistory)-1, -1, -1):
        r = undoHistory[i]
        for h in r:
            if name == h[0]:
                return h

def getName(nameIn):
    if nameIn == "":
        return None
    nameIn = nameIn.lower()
    if nameIn in nickname:
        return nickname[nameIn]
    if nameIn in rec.keys():
        return nameIn
    #deal with clashes
    for k in rec:
        if k.startswith(nameIn):
            return k
    #deal with mid-name strings
    return None

slotKeys = {
    "head": ["head", "helm"],
    "shoulder": ["shoulder", "shoulders"],
    "back": ["back", "cloak", "cape"],
    "chest": ["chest"],
    "hands": ["hand", "hands",
        "gauntlet", "gauntlets",
        "glove", "gloves"],
    "legs": ["legs", "legging",
            "leggings", "pants"]
}

def getSlot(m):
    tl = getTokens(m.lower())
    for k, v in slotKeys.items():
        for s in v:
            if s in tl:
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

async def update():
    for name in list(rec.keys()):
        print("Updating " + name.capitalize() + "...")
        try:
            ti = await Armory.getTierPieces(name)
        except RuntimeError:
            del rec[name]
            continue
        for s in ti:
            if overWrite(ti[s], rec[name][s]):
                rec[name][s] = ti[s]
    await save()

async def trade(gn, tn):
    h = searchHistory(gn)
    if h == None:
        return [gn.capitalize() +
        	    " hasn't looted anything."]
    slot = h[1]
    rStr = revertStr(gn, slot, h[2], h[3])
    a1 = (gn, slot, h[3], h[2])
    rec[gn][slot] = h[2]

    wStr = winStr(tn, slot, h[3])
    oldpiece = rec[tn][slot]
    a2 = (tn, slot, oldpiece, h[3])
    rec[tn][slot] = h[3]

    undoHistory.append([a1, a2])
    return [rStr, wStr]

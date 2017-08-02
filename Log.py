import requests
import asyncio
from misc import *
from datetime import datetime
session = requests.Session()
url = "https://www.warcraftlogs.com:443/v1/"

session.params.update({'api_key':
                 '3f248bda7726441ab32651d94f98eeea'})

def lastRaid():
    reports = []
    r = session.get(url + "reports/guild/Unified/Madoran/US")
    for item in r.json():
        reports.append(item)
    return reports[-1]['id']

oldwar = 188028
prolonged = 229206
deadlygrace = 188027
potions =  [oldwar, prolonged, deadlygrace]
rune = [224001]

class Night():
    def __init__(self, idIn):
        self.nightID = idIn
        self.pLst = []
        self.pDict = {}
        self.pulls = []

        response = session.get(url + "report/fights/" + self.nightID)
        if not response.ok:
            raise RuntimeError("Unable to fetch the log.")
        r = response.json()
        for entity in r["friendlies"] :
            if all(key != entity["type"]
                        for key in ["Pet", "NPC"]):
                self.pLst.append(entity)
                self.pDict[entity["id"]] = entity["name"]
        for pull in r["fights"]:
            if (pull['boss'] != 0
                and pull['end_time'] - pull['start_time']
                    > 40000):
                self.pulls.append(pull)
        if len(self.pulls) == 0:
            raise RuntimeError("Empty log")
        if len(self.pulls) > 50:
            raise RuntimeError("log too big")
        self.title = r["title"]
        self.time = r["start"]

    def start(self, pull = -1):
        return self.pulls[pull]['start_time']

    def end(self, pull = -1):
        return self.pulls[pull]['end_time']

    def __str__(self):
        return self.title + datetime.fromtimestamp(
                    self.time/1000).strftime(" on %a, %m/%d")

    def pullDesc(self, pullNum = -1):
        if pullNum >= len(self.pulls):
            return "We didn't do that many pulls."
        pull = self.pulls[pullNum]
        boss = pull["name"]
        killStr = " kill on " if pull["kill"] else " wipe on "
        timeStr = datetime.fromtimestamp(
                (self.time + self.end(pullNum))/1000).strftime("%H:%M%P.")
        return boss + killStr + timeStr

    tankSpecID = [66, 73, 104, 250, 268, 581]
    healSpecID = [65, 105, 256, 257, 264, 270]

    def dpsLst(self, pull = -1):
        start = self.start(pull)
        response = session.get(url + "report/events/" + self.nightID,
                    params = {"start": start, "end": start + 1})

        if not response.ok:
            raise RuntimeError("Connection Interrupted at dpsLst")

        events = response.json()["events"]
        lst = []
        for e in events:
            etype = e["type"]
            if etype == "encounterstart":
                continue
            elif etype == "combatantinfo":
                specID = e["specID"]
                if (specID not in Night.tankSpecID
                        and specID not in Night.healSpecID):
                    lst.append(e["sourceID"])
            else:
                break
        return lst

    def ppLst(self, lst):
        if len(lst) == 0:
            return "(no one)"
        nLst = []
        for p in lst:
            nLst.append(self.pDict[p])
        nLst.sort()
        return ppStrLst(nLst)

    def raidMembers(self):
        nLst = []
        for pID in self.pDict:
            nLst.append(self.pDict[pID])
        nLst.sort()
        return nLst

    def buffCounts(self, bLst, pull = -1):
        dLst = self.dpsLst(pull)

        pCounts = {}
        for d in dLst:
            pCounts[d] = 0

        rLst = []
        for b in bLst:
            rLst.append(session.get(url + "report/tables/buffs/" + self.nightID,
                params = {"start": self.start(pull),
                          "end": self.end(pull), "abilityid": b}))

        for r in rLst:
            if not r.ok:
                raise RuntimeError("Connection interrupted.")
            for p in r.json()["auras"]:
                if p["id"] in pCounts:
                    pCounts[p["id"]] += p["totalUses"]
        return pCounts

    def ppBCounts(self, bCounts):
        rLst = []
        for pID in bCounts:
            rLst.append(self.pDict[pID] + " used " + '%d' % bCounts[pID] + ".")
        return rLst

    def potionCountOutput(self, pull = -1):
        return self.ppBCounts(self.buffCounts(potions, pull))

    def runeCountOutput(self, pull = -1):
        return self.ppBCounts(self.buffCounts(rune, pull))

    def noPotionList(self, pull = -1):
        if pull >= len(self.pulls):
            return "We didn't do that many pulls."
        pCounts = self.potionCounts(pull)
        lst = []
        for pID in pCounts:
            if pCounts[pID] == 0:
                lst.append(pID)
        if len(lst) == 0:
            return "Everyone used at least one potion."
        return ("People who didn't pot up were " +
                    self.ppLst(lst) + ".")

    def noRuneList(self, pull = -1):
        if pull >= len(self.pulls):
            return "We didn't do that many pulls."
        pCounts = self.runeCounts(pull)
        lst = []
        for pID in pCounts:
            if pCounts[pID] == 0:
                lst.append(pID)
        if len(lst) == 0:
            return "Everyone runed up."
        return ("People who didn't rune up were " +
                    self.ppLst(lst) + ".")

    def avg(self, pCounts):
        if len(pCounts) == 0:
            return 0
        pSum = 0
        for pID in pCounts:
            pSum += pCounts[pID]
        return pSum / len(pCounts)

    def pullBuffStats(self, bLst, pull):
        bCounts = self.buffCounts(pull)
        average = self.avg(bCounts)
        ans = {"average" : average}
        for pID in bCounts:
            if average - bCounts[pID] > 0.5:
                ans[self.pDict[pID]] = bCounts[pID]
        return ans

    def pullPotionAnalysis(self, pull = -1):
        pCounts = self.potionCounts(pull)
        average = self.avg(pCounts)
        ans = {"average" : average}
        for pID in pCounts:
            if average - pCounts[pID] > 0.5:
                ans[self.pDict[pID]] = pCounts[pID]
        return ans

    async def buffStats(self, buffs):
        #cached buffCounts for each fight
        bcs = []

        #list of average number of buffs
        avgs = []

        #keys = pIDs
        #value = list of pulls participated
        pPulls = {}

        for i in range(len(self.pulls)):
            bc = self.buffCounts(buffs, i)
            bcs.append(bc)
            avgs.append(self.avg(bc))
            for pID in bc:
                if pID not in pPulls:
                    pPulls[pID] = [i]
                else:
                    pPulls[pID].append(i)

        #keys = pIDs
        #value = (average-of-player, overall-average-on-same-fights)
        lacks = {}

        for pID in pPulls:
            sp = 0
            sg = 0
            for pull in pPulls[pID]:
                sp += bcs[pull][pID]
                sg += avgs[pull]
            ap = sp / len(pPulls[pID])
            ag = sg / len(pPulls[pID])
            if ap - ag < -0.3:
                lacks[pID] = (ap, ag)

        if len(lacks) == 0:
            return ["Nobody was falling behind.",
                    "Our dps were using %.2f on average per pull." % ag]

        #item = (pName, lacks[player], pullCount)
        lackLst = []

        for pID in lacks:
            lackLst.append((self.pDict[pID], lacks[pID], len(pPulls[pID])))
        lackLst.sort() #by alphabetical order

        ans = []
        for item in lackLst:
            ans.append("%s used %.2f potions per pull (out of %d pulls), "
                        "while the group used %.2f on those fights."
                        % (item[0], item[1][0], item[2], item[1][1]))
        return ans

import convo
import asyncio
import random
import FaithData
import Tier
import Armory
import Log
from misc import *
from datetime import datetime

faith = None

async def silence(message):
    await faith.send_message(message.channel,
                        random.choice(["I'm sorry!", "Sorry.",
                        "Sorry! I'll be quiet."]))
    convo.endConvo(message.author)

async def reply(message):
    await convo.getReply(message.author)(message)

async def closeLog(message):
    convo.removeTopic(message.author, "log")
    await faith.send_message(message.channel, "Log closed")

async def noPot(message):
    night = convo.getTopic(message.author, "log")
    pull = getNum(message.content)
    await faith.send_message(message.channel, night.noPotionList(pull - 1))

async def potCount(message):
    pull = getNum(message.content)
    night = convo.getTopic(message.author, "log")
    await faith.send_message(message.channel,
        "Counting the potion usage for pull #%d..." % pull)
    for s in night.potionCountOutput(pull - 1):
        await faith.send_message(message.channel, s)
    await faith.send_message(message.channel, "That's all.")

async def potStats(message):
    night = convo.getTopic(message.author, "log")
    reply = random.choice(["Please give me a second.",
                           "Working on it!"])
    await faith.send_message(message.channel,
            reply)
    analysis = await night.nightPotionAnalysis()
    for s in analysis:
        await faith.send_message(message.channel, s)
    await faith.send_message(message.channel, "That's all.")

async def noRune(message):
    await faith.send_message(message.channel, "Runes NYI")

async def runeCount(message):
    await faith.send_message(message.channel, "Runes NYI")

async def runeStats(message):
    await faith.send_message(message.channel, "Runes NYI")

async def refreshLog(message):
    nID = convo.getTopic(message.author, "log").nightID
    convo.setTopic(message.author, "log", Log.Night(nID))
    await faith.send_message(message.channel, "Done refreshing.")

async def newLog(message):
    loc = message.content.find('warcraftlogs.com/reports/')
    try:
        if loc == -1:
            night = Log.Night(Log.lastRaid)
        else:
            loc += len('warcraftlogs.com/reports/')
            night = Log.Night(message.content[loc:loc+16])
    except RuntimeError:
        await faith.send_message(message.channel,
                        "I can't access that log. "
                        "Please double check the link.")
        return
    await faith.send_message(message.channel, str(night))
    convo.setTopic(message.author, "log", night)
    return

async def pullDesc(message):
    night = convo.getTopic(message.author, "log")
    pull = getNum(message.content)
    await faith.send_message(message.channel, night.pullDesc(pull))

async def pullNum(message):
    night = convo.getTopic(message.author, "log")
    await faith.send_message(message.channel,
        "We did %d pulls." % len(night.pulls))

async def participants(message):
    night = convo.getTopic(message.author, "log")
    await faith.send_message(message.channel,
        night.raidMembers())
    return

async def suggestion(message):
    await faith.send_message(message.channel,
            "Sorry, I can't handle suggestions yet.")

def winStr(name, slot, piece):
    return name.capitalize() + " won " + Tier.pToS(piece) + " " + slot + "."

async def wonPiece(message):
    if message.author.id not in officers:
        await faith.send_message("Only officers can do that.")
        return
    piece = Tier.extractPiece(message.content)
    slot = Tier.getSlot(message.content)
    loc = message.content.find(":")
    if loc == -1:
        #TODO
        await faith.send_message(message.channel,
                "This grammar/format is still in development. "
                "Please use the : format.")
    else:
        tokens = getTokens(message.content[loc:len(message.content)])
        names = []
        for t in tokens:
            if t == "and":
                continue #idiot-proof
            name = Tier.getName(t)
            if name == None:
                await faith.send_message(message.channel, "Cannot find " + t)
                continue
            names.append(name)
        for name in names:
            issues = Tier.winIssues(name, slot, piece)
            reply = "Recorded " + winStr(name, slot, piece)
            if issues:
                reply += " " + issues
            await faith.send_message(message.channel, reply)
        await Tier.award(names, slot, piece)

async def undoWin(message):
    if message.author.id not in officers:
        await faith.send_message("Only officers can do that.")
        return
    for s in await Tier.undo():
        await faith.send_message(message.channel, s)
    await faith.send_message(message.channel, "That should be all...")
    return

async def redoWin(message):
    await faith.send_message("I haven't been taught now to do that yet :(")
    return

async def deletePiece(message):
    if message.author.id not in officers:
        await faith.send_message("Only officers can do that.")
        return
    slot = Tier.getSlot(message.content)
    tokens = getTokens(message.content)
    for i in range(1, len(tokens)):
        if tokens[i] == "s":
            name = Tier.getName(tokens[i-1])
    if name == None:
        await faith.send_message(message.channel, "Can't find the player.")
        return
    oldPieceDesc = await Tier.forceOverwrite(name, slot, None)
    await faith.send_message(message.channel,
            "Deleted " + name.capitalize() + "s' "
            + oldPieceDesc + " " + slot + ".")

async def tierCount(message):
    m = message.content
    tokens = getTokens(message.content)
    name = None
    for i in range(len(tokens)):
        if tokens[i] == "does" and i+2 < len(tokens) and tokens[i+2] == "have":
            name = Tier.getName(tokens[i+1])
            break
        if tokens[i] == "s":
            name = Tier.getName(tokens[i+1])
            break
    if name == None:
        await faith.send_message(message.channel, "Player not found.")
        return

    slot = Tier.getSlot(m)
    if slot:
        await faith.send_message(message.channel,
                    name.capitalize() + " has "
                    + Tier.pieceDesc(name, slot) + " " + slot + ".")
    else:
        count = 0
        for s in Armory.slots:
            if Tier.rec[name][s] != None:
                count += 1
        await faith.send_message(message.channel,
                name.capitalize() + " has %d tier pieces." % count)
        for s in Armory.slots:
            p = Tier.rec[name][s]
            if p != None:
                await faith.send_message(message.channel,
                        s + ": " + Tier.pieceDesc(name, s))

async def raidNight(message):
    m = message.content.lower()
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
        await faith.send_message(message.channel,
                "Sorry, which difficulty again?")
    else:
        Tier.currentRaid = diff
        reply = random.choice(["Gotcha. Good luck and have fun!",
                                "Glhf! I wish I could raid too.",
                                "Go out there and get some loots!",
                                "Teach them the might of Unified!"])
        await faith.send_message(message.channel, reply)

async def raidEnd(message):
    reply = random.choice(["Good work tonight, and good night guys :)",
                            "Hope you guys had fun and got some gears!"])
    await faith.send_message(message.channel, reply)
    Tier.currentRaid = None
    return

async def newRaider(message):
    await faith.send_message(message.channel, "NYI")

async def gquit(message):
    faith.send_message(message.channel,
            ("That's too bad. "
            "I'll update my records next time when "
            "I look everyone up on the Armory."))

async def introduce(message):
    await faith.send_message(message.channel,
                            random.choice(FaithData.intros))

async def creator(message):
    faith.send_message(message.channel,
            ("Ethan and Doin taught me some basics to start with. "
                "From now on, my creator will be all of you though!"))

async def function(message):
    await faith.send_message(message.channel,
        FaithData.capabilities)

async def define(message):
    mStr = message.content.lower()
    if 'facebook' in mStr:
        await faith.send_message(message.channel,
                          FaithData.definitions['Facebook'])
    elif 'bank' in mStr:
        await faith.send_message(message.channel,
                          FaithData.bankInfo)
    elif 'guild' in mStr or 'unified' in mStr:
        await faith.send_message(message.channel,
                          FaithData.definitions['Unified'])
    elif 'hanabi' in mStr:
        await faith.send_message(message.channel,
                          FaithData.definitions['Hanabi'])
    elif 'ethan' in mStr:
        await faith.send_message(message.channel,
                          FaithData.definitions['Ethan'])
    elif 'stus' in mStr or 'about doin' in mStr:
        await faith.send_message(message.channel,
                          FaithData.definitions['Doin'])
    elif 'danny' in mStr or 'yaois' in mStr:
        await faith.send_message(message.channel,
                          FaithData.definitions['Danny'])
    elif 'my rank' in mStr:
        await faith.send_message(message.channel,
                        ("Our raiders' ranks are "
                         "posted on our Facebook group."))
    elif 'rank' in mStr or 'loot' in mStr:
        await faith.send_message(message.channel,
                          FaithData.definitions['Rank'])
    elif 'raid' in mStr:
        await faith.send_message(message.channel,
                          FaithData.definitions['Raid'])
    elif 'about you' in mStr:
        await introduce(message)
    elif (('stat' in mStr and 'pri' in mStr) or 'stats' in mStr):
        await statPri(message)
    elif 'neck ench' in mStr:
        await neck(message)
    else:
        await faith.send_message(message.channel,
                 "Sorry, I don't have any information on that.")
    return

async def statPriReply(message):
    await statPri(message)
    convo.clearReply(message.author)

async def statPri(message):
    spec = getSpec(message.content.lower())
    if spec == "unknown":
        await faith.send_message(message.channel,
                "What class/spec are you playing?")
        convo.setReply(message.author,
            ((lambda x: getSpec(x.content.lower()) != "unknown"), statPriReply))
    else:
        iv = random.choice(["Icy Veins said \"",
                        "According to Icy Veins, \""])
        await faith.send_message(message.channel,
                iv + FaithData.statprios[spec] + "\".")

async def relic(message):
    await faith.send_message(message.channel,
        FaithData.specRelics[getSpec(message.content)])

async def neckReply(message):
    await neck(message)
    convo.clearReply(message.author)

async def neck(message):
    spec = getSpec(message.content.lower())
    if spec == "unknown":
        await faith.send_message(message.channel,
                "What class/spec are you playing?")
        convo.setReply(message.author,
            ((lambda x: getSpec(x.content.lower()) != "unknown"), neckReply))
    else:
        iv = random.choice(["Icy Veins said \"",
                        "According to Icy Veins, \""])
        await faith.send_message(message.channel,
                iv + FaithData.neckenchs[spec] + "\".")

async def missingEnch(message):
    await faith.send_message(message.channel, "NYI")

async def tour(message):
    await faith.send_message(message.channel, FaithData.tourScript)

async def musicBot(message):
    await faith.send_message(message.channel, "NYI")

async def disengage(message):
    if ('thank' in message.content.lower()
            or message.content.lower().startswith('ty')):
        await faith.send_message(message.channel, "No problem!")
    elif ('never mind' in message.content.lower()
            or 'nothing' in message.content.lower()):
        await faith.send_message(message.channel, "Ok.")
    else:
        await faith.send_message(message.channel,
                            random.choice(
                                ["I hope that was helpful.",
                                 "Hope that helped!"]))
    convo.endConvo(message.author)

async def greet(message):
    name = address(message.author)
    query = random.choice(
                ["",
                 " How can I help you today?",
                 " How may I be of service?"])

    hour = datetime.now().hour
    goodhour = ("Good morning, " if hour >= 3 and hour < 12 else
                "Good afternoon, " if hour >= 12 and hour < 18 else
                "Good evening, ")

    await faith.send_message(message.channel,
                random.choice(["Hi, " + name + "!" + query,
                               "Hello, " + name + "!" + query,
                               goodhour + name + "!" + query,
                               "Greetings, " + name + "." + query])
                            )
    convo.grabAttn(message.author)

async def mention(message):
    await faith.send_message(message.channel,
            address(message.author) + ", did you call me?")

async def confuse(message):
    await faith.send_message(message.channel,
            ("I'm sorry, "
            "I can't understand that."))

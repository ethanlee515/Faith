import convo
import asyncio
import random
import FaithData
import tierInfo
import Armory
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
    await faith.send_message(message.channel, "NYI")

async def noPot(message):
    await faith.send_message(message.channel, "NYI")

async def potCount(message):
    await faith.send_message(message.channel, "NYI")

async def potStats(message):
    await faith.send_message(message.channel, "NYI")

async def noRune(message):
    await faith.send_message(message.channel, "NYI")

async def runeCount(message):
    await faith.send_message(message.channel, "NYI")

async def runeStats(message):
    await faith.send_message(message.channel, "NYI")

async def refreshLog(message):
    await faith.send_message(message.channel, "NYI")

async def newLog(message):
    await faith.send_message(message.channel, "NYI")

async def pullDesc(message):
    await faith.send_message(message.channel, "NYI")

async def pullNum(message):
    await faith.send_message(message.channel, "NYI")

async def participants(message):
    await faith.send_message(message.channel, "NYI")

async def suggestion(message):
    await faith.send_message(message.channel,
            "Sorry, I can't handle suggestions yet.")

async def wonPiece(message):
    await faith.send_message(message.channel, "wonpiece NYI")

async def undoWin(message):
    await faith.send_message(message.channel, "NYI")

async def deletePiece(message):
    await faith.send_message(message.channel, "NYI")

async def tierCount(message):
    m = message.content
    loc1 = m.find("does")
    loc2 = m.find("have")
    nameIn = m[loc1+5:loc2-1].lower()
    name = tierInfo.getName(nameIn)
    if name == None:
        await faith.send_message(message.channel, "Player not found.")
        return

    slot = tierInfo.getSlot(m)
    if slot:
        await faith.send_message(message.channel,
                    name.capitalize() + " has "
                    + tierInfo.pieceDesc(name, slot) + " " + slot + ".")
    else:
        count = 0
        for s in Armory.slots:
            if tierInfo.rec[name][s] != None:
                count += 1
        await faith.send_message(message.channel,
                name.capitalize() + " has %d tier pieces." % count)
        for s in Armory.slots:
            p = tierInfo.rec[name][s]
            if p != None:
                await faith.send_message(message.channel,
                        s + ": " + tierInfo.pieceDesc(name, s))

async def newRaider(message):
    await faith.send_message(message.channel, "NYI")

async def gquit(message):
    faith.send_message(message.channel,
            ("That's too bad. "
            "I haven't been taught how to update my records for this."))

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
        faith.conversations[message.author] = \
            Faith.convoStatus.PASSIVE
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
    await faith.send_message(message.channel, "NYI")

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

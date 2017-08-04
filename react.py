import convo
import asyncio
import random
import FaithData
import Tier
import Armory
import Log
import check
from misc import *
from datetime import datetime

async def playSong(message):
    if message.channel == faith.music:
        return

    c = message.author.voice.voice_channel
    if c == None:
        await faith.send_message(message.channel,
        	    "You need to be in a voice channel.")
        return

    if faith.vchannel == None:
        faith.vchannel = await faith.join_voice_channel(c)
    else:
        await faith.vchannel.move_to(c)

    m = message.content
    q = getQuoted(m)
    if q == None:
       loc = m.find("youtube")
       i = loc
       while i > 0 and m[i-1] != ' ':
           i -= 1
       j = loc + 7
       while j < len(m) and m[j] != ' ':
           j += 1
       q = m[i:j]
    await faith.send_message(faith.music,
    	    "!summon")
    await faith.send_message(faith.music,
    	    "!play " + q)
    convo.setTopic(message.author, "music", True)
    return

async def skipSong(message):
    await faith.send_message(faith.music, "!skip")

async def louder(message):
    await faith.send_message(faith.music, "!volume +10")

async def quieter(message):
    await faith.send_message(faith.music, "!volume -10")

async def stopMusic(msg):
    await faith.send_message(faith.music, "!pause")

async def resumeMusic(msg):
    await faith.send_message(faith.music, "!resume")

async def silence(message):
    await faith.send_message(message.channel,
                        random.choice(["I'm sorry!", "Sorry.",
                        "Sorry! I'll be quiet."]))
    convo.endConvo(message.author)

async def reply(message):
    for r in convo.getReply(message.author):
        if r[0](message):
            await r[1](message)
            return

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
    for s in await night.buffStats(Log.potions):
        await faith.send_message(message.channel, s)
    await faith.send_message(message.channel, "That's all.")

async def noRune(message):
    night = convo.getTopic(message.author, "log")
    pull = getNum(message.content)
    await faith.send_message(message.channel, night.noRuneList(pull - 1))

async def runeCount(message):
    pull = getNum(message.content)
    night = convo.getTopic(message.author, "log")
    await faith.send_message(message.channel,
        "Counting the rune usage for pull #%d..." % pull)
    for s in night.runeCountOutput(pull - 1):
        await faith.send_message(message.channel, s)
    await faith.send_message(message.channel, "That's all.")

async def runeStats(message):
    night = convo.getTopic(message.author, "log")
    reply = random.choice(["Please give me a second.",
                           "Working on it!"])
    await faith.send_message(message.channel,
            reply)
    for s in await night.buffStats(Log.rune):
        await faith.send_message(message.channel, s)
    await faith.send_message(message.channel, "That's all.")

async def refreshLog(message):
    nID = convo.getTopic(message.author, "log").nightID
    convo.setTopic(message.author, "log", Log.Night(nID))
    await faith.send_message(message.channel, "Done refreshing.")

async def newLog(message):
    loc = message.content.find('warcraftlogs.com/reports/')
    try:
        if loc == -1:
            night = Log.Night(Log.lastRaid())
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
        ppStrLst(night.raidMembers()))
    return

async def suggestion(message):
    G = message.content
    fileGuild= open("Suggestion.txt", "a+")
    fileGuild.write(G + "\n")
    fileGuild.close()
    reply = random.choice(["I'll remember that!",
                        "Thanks for the suggestion!",
                        "I'll let the officers know that."])
    await faith.send_message(message.channel, reply)

async def wonPiece(message):
    if message.author.id not in officers:
        await faith.send_message("Only officers can do that.")
        return
    piece = Tier.extractPiece(message.content)
    slot = Tier.getSlot(message.content)
    loc = message.content.find(":")
    if loc == -1:
        loc = message.content.lower().find("won")
        #todo what if not found, is that possible
        tokens = getTokens(message.content[0:loc])
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
        await faith.send_message(message.channel,
        	    Tier.winStr(name, slot, piece))
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
    name = None
    for i in range(1, len(tokens)):
        if tokens[i] == "s":
            name = Tier.getName(tokens[i-1])
            break
        if tokens[i-1] == "from":
            name = Tier.getName(tokens[i])
            break
    if name == None:
        await faith.send_message(message.channel, "Can't find the player.")
        return
    oldPieceDesc = await Tier.forceOverwrite(name, slot, None)
    await faith.send_message(message.channel,
            "Deleted " + name.capitalize() + "'s "
            + oldPieceDesc + " " + slot + ".")

async def tierCount(message):
    m = message.content.lower()
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
        await faith.send_message(message.channel,
                "Sorry, I can't get that name right...")
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
    Tier.raidOver()
    return

async def updateRec(message):
    await faith.send_message(message.channel,
                "Ok, this could take a couple minutes.")
    await faith.send_message(message.channel,
                "Please be patient.")
    lst = await Tier.update()
    await faith.send_message(message.channel,
                "Done updating my tier records from armory.")
    if len(lst) > 0:
        s = lst[0]
        for i in range(1, len(lst)):
            s += ", " + lst[i]
        await faith.send_message(faith.adminChat,
            ("Automatically removed %s from the records." % ppStrLst(lst)))

async def newRaider(message):
    if message.author.id not in officers:
        await faith.send_message(message.channel,
        	    "Welcome to our raids! I'm not allowed to update "
        	    "the records for you if you aren't an officer though.")
        return
    m = message.content
    name = getQuoted(m)
    if name == None:
        if ":" in m:
            s = m[m.find(':'), len(m)]
            name = getTokens(s)[0]
        else:
            name = ""
            tl = getTokens(m)
            for i in range(len(tl) - 1):
                if tl[i] == "named":
                    name = tl[i+1]
                    break
    if name.lower() in Tier.rec:
        await faith.send_message(message.channel,
                name.capitalize() + " is already in the records.")
        return
    try:
        await Tier.addPlayer(name)
        await faith.send_message(message.channel,
        	        "Welcome, " + name.capitalize() +
                    "! I've added you to the records.")
    except RuntimeError:
        await faith.send_message(message.channel,
        	        "Sorry, I can't add " + name
                    + " to my records for some reasons.")
    return

async def trade(message):
    verbs = ["traded", "trades",
        "gave", "gives"]
    tl = getTokens(message.content.lower())
    for v in verbs:
        if v in tl:
            vLoc = tl.index(v)
            break
    if vLoc == 0 or vLoc == len(tl) - 1:
        await faith.send_message(message.channel,
        	     "Sorry, I can't understand who traded.")
        return
    giver = Tier.getName(tl[vLoc - 1])
    if giver == None:
        await faith.send_message(message.channel,
        	    "Sorry, I can't understand who gave that piece.")
        return
    if "to" in tl:
        oLoc = tl.index("to") + 1
        if oLoc >= len(tl):
            await faith.send_message(
            	    "I'm sorry, I can't understand your grammar...")
            return
        taker = Tier.getName(tl[oLoc])
    else:
        taker = Tier.getName(tl[vLoc + 1])
    if taker == None:
        await faith.send_message(message.channel,
        	    "Sorry, I can't understand who got that piece.")
        return
    for r in await Tier.trade(giver, taker):
        await faith.send_message(message.channel, r)
    return

async def gquit(message):
    await faith.send_message(message.channel,
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

async def moreFunction(message):
    f  = random.choice(FaithData.capabilities)
    r1 = "Have I mentioned that I can " + f + "?"
    r2 = "Umm... I can " + f + "."
    r3 = "I can also " + f + "!"
    convo.setReply(message.author, (lambda x: "else" in x.content),
    	    moreFunction)
    await faith.send_message(message.channel,
        random.choice([r1, r2, r3]))

async def function(message):
    f1 = random.choice(FaithData.capabilities)
    f2 = random.choice(FaithData.capabilities)
    while f1 == f2:
        f2 = random.choice(FaithData.capabilities)
    r1 = "Umm... I can " + f1 + " and " + f2 +"?"
    r2 = "To start with, I'm able to " + f1 + " and " + f2 + "..."
    convo.setReply(message.author, (lambda x: "else" in x.content),
    	    moreFunction)
    await faith.send_message(message.channel,
        random.choice([r1, r2]))

async def define(message):
    mStr = message.content.lower()
    for key in FaithData.definitions:
        if key in mStr:
            await faith_send_message(FaithData.definitions[key])
            return
    else:
        await faith.send_message(message.channel,
                 "Sorry, I don't have any information on that.")
    return

async def statPriReply(message):
    await statPri(message)
    convo.clearReply(message.author)

async def statPri(message):
    spec = getSpec(message.content.lower())
    if not spec:
        await faith.send_message(message.channel,
                "What class/spec are you playing?")
        convo.setReply(message.author,
            (lambda x: getSpec(x.content.lower())), statPriReply)
    else:
        iv = random.choice(["Icy Veins said \"",
                        "According to Icy Veins, \""])
        await faith.send_message(message.channel,
                iv + FaithData.statprios[spec] + "\".")

async def relic(message):
    r = getRelic(message.content)
    if r:
        specs = []
        for spec in FaithData.specRelics:
            if r in FaithData.specRelics[spec]:
                specs.append(spec)
        await faith.send_message(message.channel, ppStrLst(specs))
    else:
        await faith.send_message(message.channel,
            FaithData.specRelics[getSpec(message.content)])

async def neckReply(message):
    await neck(message)
    convo.clearReply(message.author)

async def neck(message):
    spec = getSpec(message.content.lower())
    if not spec:
        await faith.send_message(message.channel,
                "What class/spec are you playing?")
        convo.setReply(message.author,
            (lambda x: getSpec(x.content.lower())), neckReply)
    else:
        iv = random.choice(["Icy Veins said \"",
                        "According to Icy Veins, \""])
        await faith.send_message(message.channel,
                iv + FaithData.neckenchs[spec] + "\".")

async def missingEnch(message):
    await faith.send_message(message.channel, "NYI")

async def tour(msg):
    await faith.send_message(msg.channel,
        "Hello! My name is Faith, and I'm your tour guide today. "
        "Are you ready?")
    convo.setReply(msg.author, check.binary, tour1)
    return

async def tour1(msg):
    if check.negative(msg):
        await faith.send_message(msg.channel,
            "Sorry! I must've misunderstood.")
        convo.clearReply(msg.author)
        return
    await faith.send_message(msg.channel,
            "Ok! The most interesting thing is our in-game calendar. "
            "All guild events are posted on there. If you have event "
            "ideas, please let me or the officers know after this tour! "
            "Ready to move on?")
    convo.setReply(msg.author, check.confirmation, tour2)

async def tour2(msg):
    await faith.send_message(msg.channel,
            "Our raid team is around 5th in horde on our server. "
            "We're always looking for more raiders! "
            "Do you want to hear about our raids?")
    convo.setReply(msg.author, check.binary, tour3)

async def tour3(msg):
    if check.negative(msg):
        await tour4(msg)
    else:
        await tourR(msg)
    return

async def tourR(msg):
    await faith.send_message(msg.channel,
        "Check the in-game calendar for raid times and requirements. "
        "Our Friday nights have the lowest requirements so that's "
        "usually a great place to start.")
    convo.setReply(msg.author, check.confirmation, tourR1)

async def tourR1(msg):
    await faith.send_message(msg.channel,
        "We distribute loots using a rank system that's based on both "
        "performance and participation. "
        "For more details, see <#274725221041307649>.")
    convo.setReply(msg.author, check.confirmation, tourR2)

async def tourR2(msg):
    await faith.send_message(msg.channel,
        "We do bench underperforming members when we struggle against a boss. "
        "If you're benched, please don't take it personally. You're always "
        "welcomed to come back for the very next raid. "
        "That's about it for raids!")
    convo.setReply(msg.author, check.confirmation, tour4)

async def tour4(msg):
    await faith.send_message(msg.channel,
        "Our guild bank is free for all. If you want something that "
        "you can't take out, please let an officer (orange rank and above) "
        "know! Try to donate when you take something out though.")
    convo.setReply(msg.author, check.confirmation, tour5)

async def tour5(msg):
    await faith.send_message(msg.channel,
        "We try to live up to our name and be a home of casuals and raiders "
        "alike, just like we've been doing in the last 7 years. "
        "Welcome to our guild!")
    convo.setReply(msg.author,
        (lambda x: "thank" in x.content.lower()),
        tour6)

async def tour6(msg):
    await faith.send_message(msg.channel, "Hope you enjoyed the tour!")
    convo.clearReply(msg.author)

async def adminLogin(message):
    convo.adminLogin(message.author)
    await faith.send_message(message.channel,
    	    "Welcome, Administrator " +
    	    message.author.display_name +
    	    	". I'm at your service.")

async def disengage(message):
    m = message.content.lower()
    if (m.startswith('thank') or m.startswith('ty ') or m == "ty"):
        await faith.send_message(message.channel, "No problem!")
    elif 'good night' in m:
    	    await faith.send_message(message.channel,
    	    	    "Good night, " + address(message.author) + ".")
    elif 'never mind' in m or 'nothing' in m:
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

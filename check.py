import convo
import Tier
import asyncio
from misc import *

def isMessage(message):
    return not message.author.bot

def affirmative(msg):
    m = msg.content.lower()
    return (any(key in getTokens(m)
        for key in ["sure", "ok", "yes", "affirmative", "yea", "yeah",
                "k", "kk", "yep", "yeap"])
                or "of course" in m)

def negative(msg):
    return any(key in getTokens(msg.content.lower())
        for key in ["not", "no", "nah", "negative", "nope"])

def confirmation(msg):
    return (affirmative(msg)
        or any(key in msg.content.lower()
            for key in ["next", "move on", "tell me"]))

def binary(msg):
    return affirmative(msg) or negative(msg)

def invoke(message):
    if not message.author.id == '190494385035673611':
        return False
    m = message.content.lower()
    if not ("your creator calls" in m or "come" in m):
        return False
    lst = ["ideal", "song", "night", "wretched", "war", "neverending",
        "by the", "in the", "blossom", "despair"]
    c = 0
    for s in lst:
        if s in m:
            c += 1
    return c >= 3

def attn(message):
    return convo.hasAttn(message.author)

def reply(message):
    rLst = convo.getReply(message.author)
    if not rLst:
        return False
    return any(r[0](message) for r in rLst)

def silence(message):
    keywords = ["shut up", "go away",
                "didn't ask", "did not ask",
                "t asking you", "t talking to you",
                "fk off", "fuck off", "stfu"]

    return (any(key in message.content.lower()
                    for key in keywords)
            or message.content.lower() == "stop")

def log(message):
    return (convo.getTopic(message.author, "log") != None
        or newLog(message))

def closeLog(message):
    m = message.content.lower()
    return (all(key in m for key in ["done with", "log"])
            or all(key in m for key in ["close", "log"]))

def potion(message):
    return "pot" in message.content.lower()

def noPot(message):
    return (any(key in message.content.lower()
                for key in ["t pot", "t use pot",
                            "no pot", "t use any pot"])
                and getNum(message.content.lower()))

def potCount(message):
    return (any(key in message.content.lower()
                for key in ["count", "usage"])
            and getNum(message.content.lower()))

def potStats(message):
    return any(key in message.content.lower()
                for key in ["night", "raid", "stat", "analy"])

def rune(message):
    return 'rune' in message.content.lower()

def noRune(message):
    return (any(key in message.content.lower()
                for key in ["t rune", "t use", "no rune"])
                and getNum(message.content.lower()))

def runeCount(message):
    return (any(key in message.content.lower()
                for key in ["usage", "count"])
            and getNum(message.content.lower()))

def runeStats(message):
    return any(key in message.content.lower()
        for key in ["night", "raid", "stat", "analy"])

def refreshLog(message):
    return 'refresh' in message.content.lower()

def newLog(message):
    m = message.content.lower()
    return ('warcraftlogs.com' in m
        or (all(key in m
            for key in ['log', 'last'])
        and any(key in m
            for key in ['raid', 'night'])))

def pull(message):
    return any(key in message.content.lower()
        for key in ["pull", "attempt"])

def pullDesc(message):
    return getNum(message.content)

def pullNum(message):
    return "how many" in message.content.lower()

def participants(message):
    return any(key in message.content.lower()
            for key in ["who were there", "member",
                    "participat"])

def suggestion(message):
    m = message.content.lower()
    return ('suggest' in m
            or 'can we' in m
            or 'could we' in m
            or "why don't we" in m)

def mentionsTier(msg):
    return (Tier.currentRaid != None
        or any(key in msg.content.lower()
            for key in ["tier", "heroic", "LFR", "normal", "mythic"]))

def wonPiece(message):
    return (Tier.getSlot(message.content)
        and Tier.extractPiece(message.content)
        and any(key in message.content.lower() for
                key in ["won", ":"]))

def undoWin(message):
    return any(key in getTokens(message.content.lower())
            for key in ["scratch", "scrap", "undo"])

def redoWin(message):
    return any(key in getTokens(message.content.lower())
            for key in ["unscratch", "unscrap", "redo"])

def deletePiece(message):
    m = message.content.lower()
    return (Tier.getSlot(m) and
            any(key in getTokens(m)
                for key in ["delete", "remove", "scrap", "scratch"])
            and ("'s" in m or "from" in m))

def tierCount(message):
    m = message.content.lower()
    return (all(key in m for key in ["does", "have"])
        or all(key in getTokens(m) for key in ["s", "pieces"]))

def raidNight(message):
    return (all(key in message.content.lower()
                for key in ["tonight", "raid"])
            or all(key in message.content
                for key in ["ToS", "raid"])
            or ("switching to" in message.content.lower()
                and Tier.currentRaid != None))

def raidEnd(message):
    m = message.content.lower()
    return ((all(key in m
                for key in ["end", "raid"])
            or "raid over" in m)
            and Tier.currentRaid != None)

def updateRec(message):
    return all(key in message.content.lower()
                for key in ["update", "armory"])

def trade(message):
    return any(t in getTokens(message.content.lower())
    	    for t in ["gave", "traded"])

def newRaider(message):
    m = message.content.lower()
    return (all(key in m for key in ["join", "us"])
    	            or "new raider" in m
                    or "new player" in m)

def gquit(message):
    m = message.content.lower()
    return ("gquit" in m
        or all(key in m for key in ["left", "guild"])
        or all(key in m for key in ["quit", "guild"]))

def introduce(msg):
    m = msg.content.lower()
    return ("you" in m and ("introduc" in m or define(msg) or 'who' in m))

def creator(message):
    return ("who created you" in message.content.lower()
                or "your creator" in message.content.lower()
                or "who made you" in message.content.lower())

def function(message):
    keywords = ["what can you do", "readme",
                "help", "what are you able to do"]
    return any(key in message.content.lower()
                for key in keywords)

def define(message):
    keywords = ["tell me about", "bit about",
                "little about",
                "what's", "what is",
                "tell us about"]
    return any(key in message.content.lower()
                    for key in keywords)

def statPri(message):
    m = message.content.lower()
    return ('stat' in m and 'pri' in m) or 'stats' in m

def relic(message):
    return ("relic" in message.content.lower()
        and (getSpec(message.content) or getRelic(message.content)))

def neck(message):
    m = message.content.lower()
    return 'ench' in m and 'neck' in m

def missingEnch(msg):
    m = msg.content.lower()
    return "missing" in m and ("gem" in m or "ench" in m)

def tour(message):
    keywords = ["tour", "show me around", "show us around"]
    return any(key in message.content.lower() for key in keywords)

def adminLogin(message):
    if message.author.id not in officers:
        return False
    return all(key in message.content.lower()
    	                for key in ["admin", "login"])

def musicBot(message):
    return (convo.getTopic(message.author, "music") != None
        or playSong(message)
        or any(key in message.content.lower()
            for key in ["music", "song"]))

def playSong(message):
    m = message.content.lower()
    return ("play" in m and ("youtube" in m or getQuoted(m)))

def skipSong(message):
    return any(key in message.content.lower()
            for key in ["skip", "next song"])

def stopMusic(msg):
    m = msg.content.lower()
    return "pause" in m or all(key in m for key in ["stop", "music"])

def resumeMusic(msg):
    return "resume" in msg.content.lower()

def louder(message):
    return "louder" in message.content.lower()

def quieter(message):
    return any(key in message.content.lower() for key in ["quieter", "softer"])

def disengage(message):
    if (message.content.lower().startswith('ty')
        and len(message.content) <= 8):
        return True

    if ('thank' in message.content.lower()
            and len(message.content) < 15):
        return True

    if ('nite' in message.content.lower()
            and len(message.content) < 6):
        return True

    if ("nothing" in message.content.lower()
            and len(message.content) < 10):
        return True

    if ((message.content.lower().startswith("no")
            or message.content.lower().startswith("nah"))
            and len(message.content) < 5):
        return True

    keywords = ["that's all", "that's it", "dismissed",
                "that is all", "that is it",
                "that's about it", "that's about all",
                "that is about it", "that is about all",
                "that should be all", "that should be it",
                "never mind", "nevermind", "nvm",
                "good night", "good nite", "goodbye"]

    return any(key in message.content.lower()
                    for key in keywords)

def greet(message):
    nongreets = ['thank', 'help', 'have']

    if any(n in message.content.lower() for n in nongreets):
        return False
    elif ('Faith' in message.content
            and len(message.content) <= 15):
        return True
    else:
        greetings = ['hey', 'morning',
                     'afternoon', 'evening',
                     "what's up"]
        for g in greetings:
            cutoff = 16 if 'Faith' in message.content else 10
            if (g in message.content.lower()
                    and len(message.content) - len(g) <= cutoff):
                return True
        return False

def mention(message):
    return ('faith' in message.content.lower() and
                len(message.content) < 15)

def confuse(message):
    return convo.isActive(message.author)

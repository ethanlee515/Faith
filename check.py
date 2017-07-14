import convo
import Tier
import asyncio
from misc import *

def isMessage(message):
    return not message.author.bot

def attn(message):
    return convo.hasAttn(message.author)

def reply(message):
    c = convo.replyCheck(message.author)
    return c(message) if c else False

def silence(message):
    keywords = ["shut up", "go away",
                "didn't ask", "did not ask",
                "t asking you", "t talking to you",
                "fk off", "fuck off", "stfu"]

    return any(key in message.content.lower()
                    for key in keywords)

def log(message):
    return ('warcraftlogs.com' in message.content.lower()
        or all(key in message.content.lower()
            for key in ['analy', 'log', 'last'])
        or convo.getTopic(message.author, "log") != None)

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
    return ('warcraftlogs.com' in message.content.lower()
        or all(key in message.content.lower()
            for key in ['analy', 'log', 'last']))

def pull(message):
    return any(key in message.content.lower() for key in ["pull", "attempt"])

def pullDesc(message):
    return getNum(message.content)

def pullNum(message):
    return "how many" in message.content.lower()

def participants(message):
    return any(key in message.content.lower()
            for key in ["who were there", "member",
                    "participat"])

def suggestion(message):
    return 'suggest' in message.content.lower()

def mentionsTier(message):
    return 'tier' in message.content.lower() or Tier.currentRaid != None

def wonPiece(message):
    return (Tier.getSlot(message.content)
        and Tier.extractPiece(message.content)
        and any(key in message.content.lower() for
                key in ["won", ":", "loot"]))

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
    return ((all(key in message.content.lower()
                for key in ["tonight", "raid"])
                and Tier.currentRaid == None)
            or ("switching to" in message.content.lower()
                and Tier.currentRaid != None))

def raidEnd(message):
    m = message.content.lower()
    return ((all(key in m
                for key in ["end", "raid"])
            or "raid over" in m)
            and Tier.currentRaid != None)

def newRaider(message):
    pass

def gquit(message):
    m = message.content.lower()
    return ("gquit" in m
        or all(key in m for key in ["left", "guild"])
        or all(key in m for key in ["quit", "guild"]))

def introduce(message):
    return (("introduc" in message.content.lower()
                and "you" in message.content)
            or ("who are you" in message.content.lower()))

def creator(message):
    return ("who created you" in message.content.lower()
                or "your creator" in message.content.lower()
                or "who made you" in message.content.lower())

def function(message):
    keywords = ["what can you do",
                "what else can you do",
                "!help", "what are you able to do",
                "what else are you able to do"]
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
        and getSpec(message.content) != "unknown")

def neck(message):
    m = message.content.lower()
    return 'ench' in m and 'neck' in m

def missingEnch(message):
    pass

def tour(message):
    keywords = ["tour", "show me around", "show us around"]
    return any(key in message.content.lower() for key in keywords)

def musicBot(message):
    pass

def disengage(message):
    if (message.content.lower().startswith('ty')
        and len(message.content) <= 8):
        return True

    if ('thank' in message.content.lower()
            and len(message.content) < 15):
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
                "never mind", "nevermind", "nvm"]

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

import convo
import tier
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
            for key in ['analy', 'log', 'last']))

def closeLog(message):
    pass

def potion(message):
    pass

def noPot(message):
    pass

def potCount(message):
    pass

def potStats(message):
    pass

def rune(message):
    pass

def noRune(message):
    pass

def runeCount(message):
    pass

def runeStats(message):
    pass

def refreshLog(message):
    pass

def newLog(message):
    pass

def pull(message):
    pass

def pullDesc(message):
    pass

def pullNum(message):
    pass

def participants(message):
    pass

def suggestion(message):
    return 'suggest' in message.content.lower()

def mentionsTier(message):
    return 'tier' in message.content.lower()

def wonPiece(message):
    return (tier.getSlot(message.content)
        and tier.extractPiece(message.content))

def undoWin(message):
    pass

def deletePiece(message):
    pass

def tierCount(message):
    m = message.content.lower()
    return all(key in m for key in ["does", "have"])

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
    pass

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

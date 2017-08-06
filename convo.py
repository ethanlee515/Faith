ACTIVE = 4
PASSIVE = 3

convos = {}

async def tick(message):
    if getReply(message.author):
        rMem = getTopic(message.author, "replyMemSpan")
        if rMem == 0:
            clearReply(message.author)
            removeTopic(message.author, "replyMemSpan")
        else:
           setTopic(message.author, "replyMemSpan", rMem - 1)
    for i in list(convos.keys()): #Otherwise can't delete while iterating
        if convos[i]["attn"] <= 0:
            del convos[i]
        elif "admin" not in convos[i]:
            convos[i]["attn"] -= 1
    if getTopic(message.author, "admin"):
        return
    if 'Faith' in message.content:
        setActive(message.author)
    elif 'faith' in message.content and message.author.id not in convos:
        convos[message.author.id] = {"attn": 0}

def setState(person, state):
    if person.id not in convos:
        convos[person.id] = {"attn": state}
    else:
        convos[person.id]["attn"] = state

def setActive(person):
    setState(person, ACTIVE)

def setPassive(person):
    setState(person, PASSIVE)

def setTopic(person, topic, content):
    convos[person.id][topic] = content

def getTopic(person, topic):
    if person.id not in convos:
        return None
    if topic in convos[person.id]:
        return convos[person.id][topic]

def removeTopic(person, topic):
    if topic in convos[person.id]:
        del convos[person.id][topic]

def setReply(person, rc, rr):
    setTopic(person, "reply", [(rc, rr)])
    setTopic(person, "replyMemSpan", 3)

def setReplies(person, replies):
    setTopic(person, "reply", replies)
    setTopic(person, "replyMemSpan", 3)

def getReply(person):
    if person.id not in convos or "reply" not in convos[person.id]:
        return None
    return convos[person.id]["reply"]

def clearReply(person):
    if "reply" in convos[person.id]:
        del convos[person.id]["reply"]

def endConvo(person):
    del convos[person.id]

def hasAttn(person):
    return person.id in convos

def isActive(person):
    if person.id in convos:
        return convos[person.id]["attn"] >= ACTIVE

def grabAttn(person):
    if getTopic(person, "admin"):
        return
    convos[person.id]["attn"] = ACTIVE + 1

async def refreshAttn(message):
    person = message.author
    if person.id in convos and convos[person.id]["attn"] < PASSIVE:
        convos[person.id]["attn"] = PASSIVE

def adminLogin(person):
    setTopic(person, "admin", True)
    setPassive(person)

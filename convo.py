ACTIVE = 4
PASSIVE = 3

convos = {}

async def tick(message):
    #tick
    for i in list(convos.keys()):
        if convos[i]["attn"] <= 0:
            del convos[i]
        else:
            convos[i]["attn"] -= 1
    if 'Faith' in message.content:
        setActive(message.author)
    if 'faith' in message.content and message.author.id not in convos:
        convos[person.id] = {"attn": 0}

def setState(person, state):
    if person not in convos:
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
    if topic in convos[person.id]:
        return convos[person.id][topic]

def removeTopic(person. topic):
    if topic in convos[person.id]:
        del convos[person.id][topic]

def setReply(person, reply):
    setTopic(person, "reply", reply)

def replyCheck(person):
    if "reply" not in convos[person.id]:
        return None
    return convos[person.id]["reply"][0]

def getReply(person):
    return convos[person.id]["reply"][1]

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
    convos[person.id]["attn"] = ACTIVE + 1

async def refreshAttn(message):
    person = message.author
    if person.id in convos and convos[person.id]["attn"] < PASSIVE:
        convos[person.id]["attn"] = PASSIVE

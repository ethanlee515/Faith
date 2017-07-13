import FaithData

def getSpec(m):
    m = m.lower()
    for spec in FaithData.specAbbrevs:
        if any(abbr in m for abbr in FaithData.specAbbrevs[spec]):
            return spec
    return "unknown"

def getNum(s):
    seen = False
    val = 0
    for c in s:
        if not c.isdigit() and seen:
            return val
        if c.isdigit():
            val *= 10
            val += int(c)
            seen = True
    return val

specialAddr = {'219510574256488449': "Lord Yaois",
               '229766287377563659': "Lady Yvis",
               '227246864766992386': "Lady Rosaree",
               '236966898468651009': "Lady Fozzyrock",
               '190494385035673611': "Master Ethan",
               '227208882240356354': "Sire Stus",
               '228659623421411329': "Shadowblade Falivash"}

officers = ['219510574256488449', #Danny
            '229766287377563659', #Yvis
            '227246864766992386', #Zee
            '236966898468651009', #Fozzy
            '190494385035673611', #Ethan
            '227208882240356354', #Doin
            '228659623421411329', #Fali
            '229783128481333249', #Chirco
            '232324612040556544', #Drakania
            '234124188510715905', #Juvelices
            '234445330844876801'] #Sawbones

def address(user):
    if user.id in specialAddr:
        return specialAddr[user.id]
    if user.id in officers:
        return "Officer " + user.display_name
    return user.display_name

def nSuffix(x):
    if x % 100 not in [11, 12, 13]:
        d = {1: "st", 2: "nd", 3:"rd"}
        y = x % 10
        if y in d:
            return d[y]
    return "th"

def getTokens(x):
    ans = []
    loc = -1
    for i in range(len(x)):
        if loc == -1:
            if x[i].isalpha():
                loc = i
        else:
            if not x[i].isalpha():
                ans.append(x[loc:i])
                loc = -1
    if loc != -1:
        ans.append(x[loc:len(x)])
    return ans

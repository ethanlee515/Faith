intros = [("Hi guys! "
          "I'm a pseudo-AI to help you "
          "with your everyday Unified needs!"),
        ("My name is Faith. "
          "I'm the head of our bots "
          "in the Unified discord server. "
          "It's my pleasure to serve you."),
        ("I am your friendly neighborhood bot in this discord server. "
            "I'm named Faith because Ethan thinks it's "
            "a beautiful name.")]

capabilities = ("I can answer simple questions about the guild "
                "and give short tours. I know everyone's stats prio too. "
                "I'll be able to work as a suggestion box soon as well. "
                "Let me know what else I can help with!")

tourScript = ("Alright! Let me show you around! "
        "We are already on our discord server. "
        "We also have a very active Facebook group called "
        "\"Madoran's Unified\" at "
        "http://fb.com/groups/unifiedmadoran/. "
        "The Orange and Legendary ranks in the guild are our "
        "officers who can help you with any questions I'm unable "
        "to answer. Also, we raid a lot. Make sure to ask me "
        "about it if you're interested.")

bankInfo = ("The higher in rank you are, the more things you'll "
            "be allowed to take from the guild bank. When you "
            "take something out, try to put something else in too. "
            "Donating to the guild bank helps you rank up; "
            "we're tracking every donation using a spreadsheet."
            "If you need something you aren't able to take, "
            "talk to an officer.")

definitions = {"Unified":
                ("We're a casual raiding guild that's been serving "
                 "Madoran and Dawnbringer ever since they've merged. "
                 "We hope to live up to our name and provide a "
                 "welcoming environment for casuals and raiders alike. "
                 "Feel free to ask me for a short tour!"),
               "Ethan":
                ("Master Ethan is a master of both automata and illusions."),
               "Hanabi":
                ("Hanabi is my sister. She's also a bot but "
                "she's very different from me. Soon we'll "
                "serve in the Unified discord server together. "
                "I hope you'll meet her soon!"),
               "Doin":
                ("Sire Stus is one of the few "
                 "who have seen my source code and taught me "
                 "directly. I've learned a lot from him."),
               "Facebook":
                ("We have an active guild Facebook group. It's "
                 "called \"Madoran's Unified\". Here's the link: "
                 "http://fb.com/groups/unifiedmadoran/"),
               "Danny":
                ("Lord Yaois is our guild master and raid leader. "
                 "Ethan thinks he's a charismatic leader who "
                 "inspires loyalty."),
               "Rank":
                ("Our loots are distributed using a rank "
                 "system that's based on both attendance and "
                 "performance. It's based on a strict points system "
                 "so there's no favorism. The details are in the pdf "
                 "in the #raid_loot_info channel."),
               "Raid":
                ("Our raids are posted on the calendar with "
                 "weapon traits and item level requirements. "
                 "We have a open-door policy, so please "
                 "feel free to sign up and join us!"
                 "We have a special loot distribution/ranking system "
                 "though, so make sure to ask me about it sometimes.")
               }

statprios = {"protection warrior": "str > haste > mast >= vers > crit",
    "fury warrior": "haste > mast > vers > str > crit",
    "arms warrior": "mast > haste > vers > str > crit",
    "frost mage": "crit (to 33.34%) > int > haste > vers > mast > crit",
    "fire mage": "int > crit >= haste > mast > vers",
    "arcane mage": "vers > crit >= haste > int > mast",
    "shadow priest": "haste > crit >= mast > vers > int",
    "discipline priest": "int > haste > crit > mast > vers",
    "holy priest": "int > mast > crit > hast > vers",
    "guardian druid": "armor > vers > mast > hast > agi > crit",
    "balance druid": "haste > mast > int > crit > vers",
    "feral druid": "agi > mast > crit > vers > haste",
    "retribution paladin": "str > haste >= crit = vers > mast",
    "restoration druid": ("(raid) int > mast > haste = crit > vers, "
                "(single-target/M+) mast >= haste > int > crit> vers"),
    "retribution paladin": "str > haste >= crit = vers > mast",
    "protection paladin": "haste > vers > mast > crit",
    "holy paladin": "int > crit > mast > vers > haste",
    "elemental shaman": "int > crit > mast > vers > haste",
    "enhancement shaman": "haste = mast > agi > vers > crit",
    "restoration shaman": "int > mast > crit > haste > vers",
    "marksmanship hunter": "mastery > crit > haste > vers",
    "beast mastery hunter": "mastery > haste/crit (depends) > vers",
    "survival hunter": "haste > mastery > crit > vers",
    "destruction warlock": ("(4-piece) haste > crit > int > vers > mast, "
                                "(without) mast > haste > int > crit > vers"),
    "affliction warlock": "mast > haste > crit > vers > int",
    "demonology warlock": "haste > int > crit = mast > vers",
    "outlaw rogue": "agi > vers > haste > crit > mast",
    "assassination rogue": ("(master poisoner/toxic blade or elaborate "
        "planning/alacrity) agi > mast > vers > crit > haste, "
        "(elaborate planning/exsanguinate) agi > vers > crit > mast > haste"),
    "subtlety rogue": "agi > mast > vers > crit > haste",
    "blood death knight": ("(survival) haste > vers > mast > crit, "
        "(damage) haste > crit > vers > mast, "
        "(balanced/recommended) haste > vers > crit > mast"),
    "frost death knight": "str > crit (until 20%) > haste = crit = mast = vers",
    "unholy death knight": "str > mast > haste (until 20%) > crit OR vers (depends)",
    "brewmaster monk": "haste (until 10%) > mast = crit > vers > haste",
    "windwalker monk": ("(single target) agi > mast > crit > vers > haste, "
                    "(aoe) agi > mast > haste > crit > vers"),
    "mistweaver monk": ("(mistweaving) int > crit > vers > haste > mast, "
                "(fistweaving) int > vers > haste >= crit > mast, "
                "(M+) int, haste = mast, vers, crit"),
    "vengeance demon hunter": ("(survival) agi > vers > mast >= haste > crit, "
                    "(damage) agi > crit >= vers >= mast >= haste, "
                    "(M+) agi > mast > vers > haste > crit"),
    "havoc demon hunter": "crit > haste > vers > agi > mast"}

neckenchs = {
    "protection warrior": "(survival) heavy hide, (damage) hidden satyr",
    "fury warrior": "hidden satyr",
    "arms warrior": "hidden satyr",
    "frost mage": "hidden satyr",
    "fire mage": "hidden satyr",
    "arcane mage": "hidden satyr",
    "shadow priest": "trained soldier",
    "disc priest": "trained soldier (or ancient priestess)",
    "holy priest": "ancient priestess",
    "guardian druid": "(survival) heavy hide, (damage) hidden satyr",
    "balance druid": "either trained soldier or claw",
    "feral druid": "hidden satyr",
    "restoration druid": "trained soldier",
    "retribution paladin": "hidden satyr",
    "protection paladin": "(survival) heavy hide, (damage) hidden satyr",
    "holy paladin": "ancient priestess",
    "elemental shaman": "hidden satyr",
    "enhancement shaman": "hidden satyr",
    "restoration shaman": "trained soldier",
    "marksmanship hunter": "trained soldier",
    "beast mastery hunter": "claw",
    "survival hunter": "hidden satyr",
    "destruction warlock": "claw",
    "affliction warlock": "trained soldier",
    "demonology warlock": "claw",
    "outlaw rogue": "hidden satyr",
    "assassination rogue": "trained soldier",
    "subtlety rogue": "hidden satyr",
    "blood death knight": "heavy hide",
    "frost death knight": "hidden satyr",
    "unholy death knight": "trained soldier",
    "brewmaster monk": "heavy hide",
    "windwalker monk": "hidden satyr",
    "mistweaver monk": ("(mistweaving or fistweaving) ancient priestess, "
            "(M+) trained soldier"),
    "vengeance demon hunter": "(survival) heavy hide, (damage) hidden satyr",
    "havoc demon hunter": "claw"}

specAbbrevs = {"protection warrior": ["prot w", "protection w"],
    "fury warrior":  ["fury"],
    "arms warrior": ["arms"],
    "frost mage": ["frost m"],
    "fire mage": ["fire"],
    "arcane mage": ["arcane"],
    "shadow priest": ["spriest", "shadow", "tentacle"],
    "discipline priest": ["disc"],
    "holy priest": ["holy priest"],
    "guardian druid": ["bear", "guardian"],
    "balance druid": ["oomkin", "bird", "balance"],
    "feral druid": ["feral", "cat", "kitty"],
    "restoration druid": ["resto d", "restoration d"],
    "retribution paladin": ["ret"],
    "protection paladin": ["prot p", "protection p"],
    "holy paladin": ["holy p", "hpal"],
    "elemental shaman": ["ele"],
    "enhancement shaman": ["enh"],
    "restoration shaman": ["resto s", "restoration s"],
    "marksmanship hunter": ["mm h", "marks"],
    "beast mastery hunter": ["bm", "beast"],
    "survival hunter": ["surv"],
    "affliction warlock": ["aff"],
    "destruction warlock": ["destr"],
    "demonology warlock": ["demo"],
    "outlaw rogue": ["outlaw"],
    "assassination rogue": ["sin", "ass"],
    "subtlety rogue": ["sub"],
    "blood death knight": ["blood"],
    "frost death knight": ["frost d"],
    "unholy death knight": ["unholy"],
    "brewmaster monk": ["bm", "brew"],
    "windwalker monk": ["ww", "wind"],
    "mistweaver monk": ["mw", "mist"],
    "vengeance demon hunter": ["ven"],
    "havoc demon hunter": ["havoc"]}

officerIDs = ['219510574256488449',
            '229766287377563659',
            '227246864766992386',
            '236966898468651009',
            '190494385035673611',
            '227208882240356354',
            '228659623421411329',
            '229783128481333249',
            '232324612040556544',
            '234124188510715905',
            '234445330844876801']

specRelics = {"blood death knight": "blood, shadow, iron",
        "frost death knight": "frost, shadow, frost",
        "unholy death knight": "fire, shadow, blood",
        "arcane mage": "arcane, frost, arcane",
        "fire mage": "fire, arcane, fire",
        "frost mage": "frost, arcane, frost",
        "assassination rogue": "shadow, iron, blood",
        "outlaw rogue": "blood, iron, storm",
        "subtlety rogue": "fel, shadow, fel",
        "havoc demon hunter": "fel, shadow, fel",
        "vengeance demon hunter": "iron, arcane, fel",
        "brewmaster monk": "life, storm, iron",
        "mistweaver monk": "frost, life, storm",
        "windwalker monk": "storm, iron, storm",
        "elemental shaman": "storm, frost, storm",
        "enhancement shaman": "fire, iron, storm",
        "restoration shaman": "life, frost, life",
        "balance druid": "arcane, life, arcane",
        "feral druid": "frost, blood, life",
        "guardian druid": "fire, blood, life",
        "restoration druid": "life, frost, life",
        "holy paladin": "holy, life, holy",
        "protection paladin": "holy, iron, arcane",
        "retribution paladin": "holy, fire, holy",
        "affliction warlock": "shadow, blood, shadow",
        "demonology warlock": "shadow, fire, fel",
        "destruction warlock": "fel, fire, fel",
        "beast mastery hunter": "storm, arcane, iron",
        "marksmanship hunter": "storm, blood, life",
        "survival hunter": "storm, iron, blood",
        "discipline priest": "holy, shadow, holy",
        "holy priest": "holy, life, holy",
        "shadow priest": "shadow, blood, shadow",
        "arms warrior": "iron, blood, shadow",
        "fury warrior": "fire, storm, iron",
        "protection warrior": "iron, blood, fire"}

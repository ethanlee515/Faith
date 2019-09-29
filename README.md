# Faith

Discord chatbot for the WoW Guild Unified-Madoran/Dawnbringer

No longer maintained.

## How to run

TODO I don't think anyone will run this anyways...
* A bunch of python3 libraries... It's probably not too hard to find out just by repeatly trying to run the project and pip install what's missing.
* A bot token from Discord
* `python3 Faith.py`

## Functionalities

* Conversational/attention system. Grab her attention by calling her name. There are "active" and "passive" types of attention, depending on if you've just called her name. There's also "administrator" attention that's only available to guild officers, which lasts indefinitely. Attention is lost when enough messages have passed or when you end the conversation with her with phrases such as "that's all" or "dismissed".
* Gives simple tour of the guild (i.e. shows Facebook group)
* Stats priority (doesn't automatically update, unfortunately)
* Simple warcraftlogs analysis
	* Potion count
	* Runes count
* Simple tier-set pieces tracking
	* self-updates from WoW armory
	* Updates using conversational system
* Suggestion box for the guild

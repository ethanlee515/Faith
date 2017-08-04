import discord
import asyncio
import convo
import check
import react

convoFlow = (check.isMessage, [
    (convo.tick, None),
    (check.invoke, react.adminLogin),
    (check.attn, [
        (check.reply, react.reply),
        (check.silence, react.silence),
        (check.suggestion, react.suggestion),
        (check.log, [
            (check.closeLog, react.closeLog),
            (check.potion, [
                (check.noPot, react.noPot),
                (check.potCount, react.potCount),
                (check.potStats, react.potStats)
            ]),
            (check.rune, [
                (check.noRune, react.noRune),
                (check.runeCount, react.runeCount),
                (check.runeStats, react.runeStats)
            ]),
            (check.refreshLog, react.refreshLog),
            (check.newLog, react.newLog),
            (check.pull, [
                (check.pullDesc, react.pullDesc),
                (check.pullNum, react.pullNum)
            ]),
            (check.participants, react.participants)
        ]),
        (check.newRaider, react.newRaider),
        (check.mentionsTier, [
            (check.wonPiece, react.wonPiece),
            (check.deletePiece, react.deletePiece),
            (check.undoWin, react.undoWin),
            (check.redoWin, react.redoWin),
            (check.trade, react.trade),
            (check.raidEnd, react.raidEnd),
            (check.tierCount, react.tierCount)
        ]),
        (check.raidNight, react.raidNight),
        (check.updateRec, react.updateRec),
        (check.gquit, react.gquit),
        (check.introduce, react.introduce),
        (check.creator, react.creator),
        (check.function, react.function),
        (check.statPri, react.statPri),
        (check.relic, react.relic),
        (check.neck, react.neck),
        (check.missingEnch, react.missingEnch),
        (check.tour, react.tour),
        (check.define, react.define),
        (check.adminLogin, react.adminLogin),
        (check.musicBot, [
            (check.playSong, react.playSong),
            (check.skipSong, react.skipSong),
            (check.stopMusic, react.stopMusic),
            (check.resumeMusic, react.resumeMusic),
            (check.louder, react.louder),
            (check.quieter, react.quieter)
        ]),
        (check.disengage, react.disengage),
        (check.greet, react.greet),
        (check.mention, react.mention)
    ], convo.refreshAttn),
    (check.confuse, react.confuse)
])

async def trav(tree, message):
    if tree[1] == None:
        await tree[0](message)
        return False
    if tree[0](message):
        if type(tree[1]) == list:
            for subtree in tree[1]:
                if await trav(subtree, message):
                    if len(tree) == 3:
                        await tree[2](message)
                    return True
        else:
            await tree[1](message)
            return True

class Faith(discord.Client):

    async def on_ready(self):
        print("Yawn... Good morning?\n")
        self.music = self.get_channel('299411775835734016')
        self.adminChat = self.get_channel('239909252804771841')
        self.vchannel = None
        return

    async def on_message(self, message):
        await trav(convoFlow, message)

faith = Faith()
react.faith = faith
faith.run("MzI4NjM2MDE5ODYxNjE4Njk5.DF6tzA.gHMihRNP4slzj8ikBlbTqoIiZ2w")

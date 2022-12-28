##############################################################
##                      UNUSED                              ##
##      Code kinda broken, someone might fix later <3       ##
##                    - PearlCodes                          ##
##############################################################
from discord.ext import commands
from profanity_check import predict, predict_prob
import regex

class Profanity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    #def on_message(self, message):
    #    asyncio.run(self.on_message_no(message))
    async def on_message(self, message):
        content = message.content
        if ('fuck' in message.content) or ('shit' in message.content) or ('stupid' in message.content):
            content = re.sub(' (fuck|shit|stupid)', '', content) # don't delete space in front
        author = message.author
        #content = message.content
        if predict_prob([content])[0] > 0.75:
            try:
                await message.delete()
            except:
                pass
            dm = await self.bot.create_dm(message.author)
            await dm.send(f"please refrain from using the word(s) you have just typed: {message.content}")

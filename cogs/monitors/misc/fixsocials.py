import asyncio
import re
from aiocache import cached
import aiohttp

import discord
from data.services import guild_service
from discord.ext import commands
from utils import cfg


class FixSocials(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # regex for tiktok urls
        self.tiktok_pattern = re.compile(r"https:\/\/(www.)?((vm|vt).tiktok.com\/[A-Za-z0-9]+|tiktok.com\/@[\w.]+\/video\/[\d]+\/?|tiktok.com\/t\/[a-zA-Z0-9]+\/)")

        # regex for instagram urls
        self.instagram_pattern = re.compile(r"(https:\/\/(www.)?instagram\.com\/(?:p|reel)\/([^/?#&]+))\/")

        # twitter regex
        self.twitter_pattern = re.compile(r"https:\/\/(www.)?twitter\.com\/[A-Za-z0-9]+\/status\/[0-9]+", re.IGNORECASE)


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild:
            return
        if message.author.bot:
            return

        message_content = message.content.strip("<>")
        if tiktok_match := self.tiktok_pattern.search(message_content):
            link = tiktok_match.group(0)
            print(f"link found:")
            print(f"type: TikTok")
            print(f"link: {link}")
            await self.fix_tiktok(message, link) 
        if instagram_match := self.instagram_pattern.search(message_content):
            link = instagram_match.group(0)
            print(f"link found:")
            print(f"type: Instagram")
            print(f"link: {link}")
            await self.fix_instagram(message, link)
        if twitter_match := self.twitter_pattern.search(message_content):
            link = twitter_match.group(0)
            print(f"link found:")
            print(f"type: Twitter")
            print(f"link: {link}")
            await self.fix_twitter(message, link)

    @cached(ttl=3600)
    async def get_tiktok_redirect(self, link: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(link, allow_redirects=False) as response:
                if response.status != 301:
                    return
            
                redirected_url = str(response).split("Location': \'")[1].split("\'")[0]
        
        redirected_url = redirected_url.replace('www.tiktok.com', 'vxtiktok.com')
        if (tracking_id_index := redirected_url.index('?')) is not None:
            # remove everything after the question mark (tracking ID)
            redirected_url = redirected_url[:tracking_id_index]

        return redirected_url

    async def fix_tiktok(self, message: discord.Message, link: str):
        redirected_url = await self.get_tiktok_redirect(link)
        if redirected_url is None:
            return

        await message.reply(f"based tiktok user, seems you forgot to vx that shit. Here you go! {redirected_url}")
        await asyncio.sleep(0.5)
        await message.edit(suppress=True)

    async def fix_instagram(self, message: discord.Message, link: str):
        link = link.replace("www.", "")
        link = link.replace("instagram.com", "ddinstagram.com")

        # get video id from link
        await message.reply(f"based instagram user, seems you forgot to dd that shit. Here you go! {link}")
        await asyncio.sleep(0.5)
        await message.edit(suppress=True)

    async def fix_twitter(self, message: discord.Message, link: str):
        link = link.replace("www.", "")
        link = link.replace("twitter.com", "fxtwitter.com")

        # get video id from link
        await message.reply(f"based twitter user, seems you forgot to fx that shit. Here you go! {link}")
        await asyncio.sleep(0.5)
        await message.edit(suppress=True)


async def setup(bot):
    await bot.add_cog(FixSocials(bot))

import discord
from discord.ext import commands
import os
import praw

reddit = praw.Reddit(
    client_id=os.getenv("reddit_client_id"),
    client_secret=os.getenv("reddit_client_secret"),
    user_agent=os.getenv("reddit_user_agent"))


class NSFW(commands.Cog):
    def __init__(self, client):
        self.client = client

    #NSFW COMMANDS
    @commands.command()
    async def rnsfw(self, ctx):  #random nsfw
        if ctx.message.channel.is_nsfw():
            submission = reddit.subreddit(
                "gettingherselfoff").random()  #can also use holdthemoan
            '''embed = discord.Embed(
                description=
                f'[{submission.title}](https://www.reddit.com/r/gettingherselfoff/comments/{submission}/)',
                colour=discord.Colour.magenta())

            embed.set_image(url=submission.url)
            embed.set_footer()

            await ctx.send(embed=embed)'''
            await ctx.send(submission.url)
        else:
            await ctx.send("Use this command in a NSFW channel")

    @commands.command(aliases=['boob', 'boobies'])
    async def boobs(self, ctx):
        if ctx.message.channel.is_nsfw():
            submission = reddit.subreddit("boobs").random()
            await ctx.send(submission.url)
        else:
            await ctx.send("Use this command in a NSFW channel")

    @commands.command()
    async def pussy(self, ctx):
        if ctx.message.channel.is_nsfw():
            submission = reddit.subreddit("pussy").random()
            await ctx.send(submission.url)
        else:
            await ctx.send("Use this command in a NSFW channel")

    @commands.command()
    async def porn(self, ctx):
        if ctx.message.channel.is_nsfw():
            submission = reddit.subreddit("porn").random()
            await ctx.send(submission.url)
        else:
            await ctx.send("Use this command in a NSFW channel")


def setup(client):
    client.add_cog(NSFW(client))

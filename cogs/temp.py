import discord
from discord.ext import commands
import asyncio


class Temp(commands.Cog):
    def __init__(self, client):
        self.client = client

    #MODERATION COMMANDS
    @commands.command()
    async def temp(self, ctx, amount=1):
        embed = discord.Embed()
        embed.set_image(url = 'http://localhost/p1.jpeg')

        msg = await ctx.send(embed=embed)

        embed.set_image(url = 'attachment://p2.jpg')

        await asyncio.sleep(3)
        await msg.edit(file = discord.File('p2.jpg'),embed=embed)


def setup(client):
    client.add_cog(Temp(client))

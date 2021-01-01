import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    #OWNER COMMANDS
    @commands.command()
    async def load(self, ctx, extension):
        if (self.client.author_id == ctx.message.author.id):
            self.client.load_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} has been loaded')
        else:
            await ctx.send("You're not the author of the bot")

    @load.error
    async def load_error(self, ctx, error):
        await ctx.send(
            f'Either the file has already been loaded or it does not exist.')

    @commands.command()
    async def unload(self, ctx, extension):
        if (self.client.author_id == ctx.message.author.id):
            self.client.unload_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} has been unloaded')
        else:
            await ctx.send("You're not the author of the bot")

    @unload.error
    async def unload_error(self, ctx, error):
        await ctx.send(
            f'Either the file has already been unloaded or it does not exist.')

    @commands.command()
    async def reload(self, ctx, extension):
        if (self.client.author_id == ctx.message.author.id):
            self.client.unload_extension(f'cogs.{extension}')
            self.client.load_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} has been reloaded')
        else:
            await ctx.send("You're not the author of the bot")

    @reload.error
    async def reload_error(self, ctx, error):
        await ctx.send(
            f'Either the file has not been loaded or it does not exist.')


def setup(client):
    client.add_cog(Owner(client))

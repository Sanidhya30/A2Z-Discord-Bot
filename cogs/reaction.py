import discord
from discord.ext import commands
import random
import asyncio
import pymongo
import os

mongo_client = pymongo.MongoClient(os.getenv("mongo_uri"))
react_db = mongo_client.A2Z_discord.question_reaction_channel

class Reaction(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        #print(ctx.content)

        #by pymongo
        react_db.find_one({"channel_id": ctx.channel.id})

        if (react_db.find_one({
                "channel_id": ctx.channel.id
        }) is not None):
        #channel_id = 767596050516017183

        #if(ctx.channel.id == channel_id):
            #print("hello")
            await ctx.add_reaction('🇦')
            await ctx.add_reaction('🇧')
            await ctx.add_reaction('🇨')
            await ctx.add_reaction('🇩')
            await ctx.add_reaction('❓')


    #Reaction COMMANDS
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reaction_start(self, ctx):

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        await ctx.send('Please mention the channel name/id.')

        try:
            msg = await self.client.wait_for(
                'message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(
                "You didn\'t answer in time, please be quicker next time!")
            return
        else:
            if msg.content == 'cancel':
                await ctx.send('The reactions is cancelled')
                return
            #print("hello1")
            channel = msg.content

        #print(channel)
        try:
            channel_id = int(channel[2:-1])
        except:
            await ctx.send(
                f'You didn\'t mention the channel name properly, Please mention like {ctx.channel.mention} next time!'
            )
            return
        else:
            channel = self.client.get_channel(channel_id)


        if type(channel_id) is int:
            #print("hello")
            react_db.update_one({
                "channel_id": channel_id
            }, {"$set": {
                "channel_id": channel_id
            }},
                              upsert=True)


    @reaction_start.error
    async def reaction_start_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry you are not allowed to use this command.')


def setup(client):
    client.add_cog(Reaction(client))

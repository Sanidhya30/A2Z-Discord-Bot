import discord
from discord.ext import commands
import random
import asyncio
from replit import db


class GTN(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        #print(ctx.content)
        if ctx.channel.id in db.keys() and ctx.content.isdigit():
            if int(ctx.content) == db[ctx.channel.id]:
                new_embed = discord.Embed(
                    description=f'🎉{ctx.author.mention} guessed it right!The number was {db[ctx.channel.id]}',
                    colour=discord.Colour.gold())

                new_embed.set_author(name = ctx.author, icon_url=ctx.author.avatar_url)

                await ctx.channel.set_permissions(
                    ctx.guild.default_role, send_messages=False)
                await ctx.channel.send(embed=new_embed)

                del db[ctx.channel.id]

                #await ctx.channel.send(embed=new_embed)

                embed = discord.Embed(
                    description=f'🎉Congratulations you won the gtn event in {ctx.channel.mention}🎉',
                    colour=discord.Colour.gold())
                await ctx.author.send(embed=embed)

    #GTN COMMANDS
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def gtnstart(self, ctx):
        questions = [
            'Specify the channel name in which you want this game to take place',
            'Specify the minimum limit', 'Specify the maximum limit'
        ]

        answers = []

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        embed = discord.Embed(
            title='🔢 Guess The Number 🔢', colour=discord.Colour.dark_teal())

        for i in questions:
            embed.set_footer(text="Type 'cancel' to cancel the gtn")
            embed.clear_fields()
            embed.add_field(
                name=f"{i}", value="(Please answer within 30 seconds)")

            await ctx.send(embed=embed)

            try:
                msg = await self.client.wait_for(
                    'message', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(
                    "You didn\'t answer in time, please be quicker next time!")
                return
            else:
                if msg.content == 'cancel':
                    await ctx.send('The gtn is cancelled')
                    return
                answers.append(msg.content)

        try:
            channel_id = int(answers[0][2:-1])
        except:
            await ctx.send(
                f'You didn\'t mention the channel name properly, Please mention like {ctx.channel.mention} next time!'
            )
            return
        else:
            channel = self.client.get_channel(channel_id)

        if not (answers[1].isdigit() and answers[2].isdigit()):
            await ctx.send(
                "You didn\'t mentioned the minimum or maximum range properly. Please mention next time!'"
            )
            return
        else:
            number = random.randint(int(answers[1]), int(answers[2]))
            db[channel_id] = number

            new_embed = discord.Embed(
                description=
                f'The game will start in one minute in {channel.mention}',
                colour=discord.Colour.dark_purple())

            #await ctx.send(embed=new_embed)

            await ctx.author.send(f'The number is {number}')

            await channel.set_permissions(
                ctx.guild.default_role, send_messages=False)
            await channel.send(embed=new_embed)

            await asyncio.sleep(1)

            await channel.set_permissions(
                ctx.guild.default_role, send_messages=True)
            new_embed.title = 'Game has started'
            new_embed.description = f'The range is from `{answers[1]}` to `{answers[2]}`'
            await channel.send(embed=new_embed)


def setup(client):
    client.add_cog(GTN(client))

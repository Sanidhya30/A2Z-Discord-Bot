import discord
from discord.ext import commands
import asyncio
import random


def convert(time):
    pos = ['s', 'h', 'm', 'd']

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]


class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client

    #GIVEAWAY COMMANDS
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def gstart(self, ctx):
        questions = [
            "Mention the channel you want to host the giveaway in.",
            "Mention the duration of the giveaway (s|m|h|d)",
            "Mention the prize of the giveaway",
            "Mention the number of winners"
        ]

        answers = []

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        embed = discord.Embed(
            title="🎉Giveaway🎉", colour=discord.Colour.magenta())

        for i in questions:
            embed.set_footer(text="Type **cancel** to cancel the giveaway")
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
                    await ctx.send('The giveaway is cancelled')
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

        time = convert(answers[1])

        if time == -1:
            await ctx.send(
                f"You didn\'t mentioned a proper unit(s|m|d|h). Please mention next time!"
            )
            return
        elif time == -2:
            await ctx.send(
                f"You didn\'t entered the proper value of time. Please mention next time!"
            )
            return

        if not answers[3].isdigit():
            await ctx.send(
                "You didn\'t mentioned the number of winners properly. Please mention next time!'"
            )
            return
        embed.clear_fields()
        embed.description = f'🎁 The prize is **{answers[2]}**\n👑 **{answers[3]}** Winners\n 🕶️ Hosted by {ctx.author.mention}'
        embed.set_footer(text=f"⏲️ Ends in {answers[1]} from now!")

        message = await channel.send(embed=embed)
        await message.add_reaction('🎉')

        await asyncio.sleep(time)

        new_msg = await channel.fetch_message(message.id)

        users = await new_msg.reactions[0].users().flatten()
        #print(users, type(users))

        users.pop(users.index(self.client.user))
        #print(users)

        if not users:
            await channel.send("Couldn\'t determine a winner")
            return

        winners = random.choices(users, k=int(answers[3]))
        print((winners))

        #[{submission.title}](https://www.reddit.com/r/memes/comments/{submission}/)

        new_winner_var = ""
        new_embed = discord.Embed(description = f"**Congratulations** you won a giveaway in {channel.mention}",colour = discord.Colour.gold())
        #new_embed.add_field(f"Congratulations")
        for i in (winners):
            await i.send(embed=new_embed)
            new_winner_var += "<@" + str(i.id) + "> "

        #print(winners[0].id)

        

        await channel.send(
            f"🎉*Congratulations* {new_winner_var} you won **{answers[2]}**!!!🎉"
        )

    @gstart.error
    async def gstart_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry you are not allowed to use this command.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def greroll(self, ctx):
        questions = [
            "Mention the channel name(within 30 seconds)",
            "Mention the message id of that giveaway(within 30 seconds)",
            "Mention the number of winners you want to reroll(within 30 seconds)"
        ]
        answers = []

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.client.wait_for(
                    'message', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(
                    "You didn\'t answer in time, please be quicker next time!")
                return
            else:
                answers.append(msg.content)

        #print(answers[0],answers[1])

        try:
            channel_id = int(answers[0][2:-1])
        except:
            await ctx.send(
                f'You didn\'t mention the channel name properly, Please mention like {ctx.channel.mention} next time!'
            )
            return
        else:
            channel = self.client.get_channel(channel_id)

        try:
            new_msg = await channel.fetch_message(int(answers[1]))
        except:
            await ctx.send("The id was entered incorrectly.")
            return

        if not answers[2].isdigit():
            await ctx.send(
                "You didn\'t mentioned the number of winners properly. Please mention next time!'"
            )
            return

        users = await new_msg.reactions[0].users().flatten()

        users.pop(users.index(self.client.user))

        if not users:
            await channel.send("Couldn\'t determine a winner")
            return

        winners = random.choices(users, k=int(answers[2]))

        new_winner_var = ""
        new_winner_var = ""
        new_embed = discord.Embed(description = f"**Congratulations** you won a giveaway in {channel.mention}",colour = discord.Colour.gold())

        for i in (winners):
            await i.send(embed=new_embed)
            new_winner_var += "<@" + str(i.id) + "> "

        await channel.send(
            f"🎉*Congratulations* {new_winner_var} you won **{answers[2]}**!!!🎉"
        )

    @greroll.error
    async def greroll_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry you are not allowed to use this command.')


def setup(client):
    client.add_cog(Giveaway(client))

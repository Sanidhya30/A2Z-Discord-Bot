import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    #MODERATION COMMANDS
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        if amount > 0:
            amount = amount + 1
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"Deleted {amount-1} messages!")
        else:
            await ctx.send("Please enter the value greater than 0")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry you are not allowed to use this command.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f"{member} Tata-bye-bye!!")
        except:
            await ctx.send('Sorry you are not allowed to use this command.')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry you are not allowed to use this command.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member} Tata-bye-bye-Foreverrr!!")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry you are not allowed to use this command.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        #print(banned_users)
        #print(banned_users[0])

        if '#' in member:
            member_name, member_hash = member.split('#')

            for ban_entry in banned_users:
                user = ban_entry.user
                #print(user,user.name,user.discriminator,user.id)

                if user.name == member_name and user.discriminator == member_hash:
                    await ctx.guild.unban(user)
                    await ctx.send(
                        f"{user.name}#{user.discriminator} has been unbanned!!!!  WOoooho"
                    )
                    break
        else:
            member = int(member)
            for ban_entry in banned_users:
                user = ban_entry.user
                if user.id == member:
                    await ctx.guild.unban(user)
                    await ctx.send(
                        f"{user.name}#{user.discriminator} has been unbanned!!!!  WOoooho"
                    )
                    break

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry you are not allowed to use this command.')


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, amount=0):
        await ctx.channel.edit(slowmode_delay = int(amount))
        #print(ctx.channel.slowmode_delay)
        await ctx.send(f'The slowmode is set to {amount} seconds')

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry you are not allowed to use this command.')

    
    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def lockdown(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send( ctx.channel.mention + " ***is now in lockdown.***")

    @lockdown.error
    async def lockdown_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry you are not allowed to use this command.')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(ctx.channel.mention + " ***has been unlocked.***")
        #print(ctx.author)
        #await ctx.author.send('yo')

    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Sorry you are not allowed to use this command.')
        

    '''@commands.command()
    async def display(ctx):
      banned_users = await ctx.guild.bans()
      await ctx.send(banned_users)'''
    """@client.event
    async def on_message(message):
        if message.author == client.user:
          return

        msg = message.content

        if msg.startswith(prefix):
          msg = msg.replace('$','',1)
          if msg.startswith("ping"):
            await message.channel.send("pong")"""


def setup(client):
    client.add_cog(Moderation(client))

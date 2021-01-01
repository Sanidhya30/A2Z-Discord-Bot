import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from replit import db
import datetime
import pytz

#TIC-TAC-TOE
#PRIVATE NOTE SETTING LIKE STICKY NOTES
#gtn (add some feature like hint)
#server-info, user-info


def get_prefix(client, message):
    if str(message.guild.id) in db.keys():
        return db[f"{str(message.guild.id)}"]
    else:
        db[f"{str(message.guild.id)}"] = '-'
        return '.'


client = commands.Bot(
    command_prefix=get_prefix,
    case_insensitive=True,
    intents=discord.Intents.all())

client.remove_command('help')
client.author_id = 241887432855781377


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Hello Noob!"))
    print(f"We are logged in as {client.user}")


@client.event
async def on_guild_join(guild):
    db[f"{str(guild.id)}"] = '.'


@client.event
async def on_guild_remove(guild):
    del db[f"{str(guild.id)}"]

@client.event
async def on_command_error(ctx, error):
    IST = pytz.timezone('Asia/Kolkata') 
    print(f'The error was {error}, time of the error {datetime.datetime.now(IST)}')

@client.event
async def on_message(ctx):
    if client.user.mentioned_in(ctx):
        await ctx.channel.send(f"My prefix is `{get_prefix(client, ctx)}`")
    else:
        await client.process_commands(ctx)

@client.command()
async def prefix(ctx, pre):  #for setting the server prefix
    db[f"{str(ctx.guild.id)}"] = pre
    #print(db[f"{str(ctx.guild.id)}"])
    await ctx.send(f'The new prefix is `{pre}`')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
client.run(os.getenv("token"))

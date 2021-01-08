import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
#from replit import db
import datetime
import pytz
import pymongo

#TIC-TAC-TOE store the last 5 matches result
#server-info, user-info
#giveaway store in the database

mongo_client = pymongo.MongoClient(os.getenv("mongo_uri"))
server = mongo_client.A2Z_discord.server_prefix


def get_prefix(client, message):  #retrieving prefix from database
    #implemented by pymongo
    prefix = server.find_one({
        "server_id": str(message.guild.id)
    }, {
        "prefix": 1,
        "_id": 0
    })

    if prefix is not None:
        return prefix.get("prefix")
    else:
        server.insert_one({"server_id": str(message.guild.id), "prefix": "-"})
        return "-"

    #implemented by replit
    '''if str(message.guild.id) in db.keys():
        return db[f"{str(message.guild.id)}"]
    else:
        db[f"{str(message.guild.id)}"] = '-'
        return '-'''


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
    server.insert_one({"server_id": str(guild.id), "prefix": "-"})  #pymongo
    #db[f"{str(guild.id)}"] = '-'


@client.event
async def on_guild_remove(guild):
    server.delete_one({"server_id": str(guild.id)})  #pymongo
    #del db[f"{str(guild.id)}"]  replit database


@client.event
async def on_command_error(ctx, error):
    IST = pytz.timezone('Asia/Kolkata')
    print(
        f'The error was {error}, time of the error {datetime.datetime.now(IST)}'
    )


@client.event
async def on_message(ctx):
    if client.user.mentioned_in(ctx):
        await ctx.channel.send(f"My prefix is `{get_prefix(client, ctx)}`")
    else:
        await client.process_commands(ctx)


@client.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, pre):  #for setting the server prefix

    server.update_one({
        "server_id": str(ctx.guild.id)
    }, {"$set": {
        "server_id": str(ctx.guild.id),
        "prefix": pre
    }},
                      upsert=True)

    '''db[f"{str(ctx.guild.id)}"] = pre
    print(db[f"{str(ctx.guild.id)}"])''' #replit database
    await ctx.send(f'The new prefix is `{pre}`')


@prefix.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry you are not allowed to use this command.')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
client.run(os.getenv("token"))

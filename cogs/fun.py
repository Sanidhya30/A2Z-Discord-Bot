import discord
from discord.ext import commands
import os
import requests  #to import api module
import aiohttp  #to import api module
import io
import praw


def get_number_facts():
    response = requests.get("http://numbersapi.com/random/trivia?json")
    #print(response.status_code)
    temp = response.json()
    #print(type(temp))
    #print(temp['text'])
    #print(temp[0]['text'])
    #json_data = json.loads(response.text)
    #print(json_data,type(json_data))
    return (temp['text'])


def get_general_facts():
    response = requests.get("https://useless-facts.sameerkumar.website/api")
    temp = response.json()
    #print(temp)
    return temp['data']


reddit = praw.Reddit(
    client_id=os.getenv("reddit_client_id"),
    client_secret=os.getenv("reddit_client_secret"),
    user_agent=os.getenv("reddit_user_agent"))


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    '''@commands.Cog.listener()
    async def on_ready(self):
        print("We are logged in as {0.user}".format(self.client))'''

    #FUN COMMANDS
    @commands.command()
    async def ping(
            self,
            ctx):  #Use {prefix}ping, A ping command used to check latency
        await ctx.send(f"Pong! {round(self.client.latency*1000)}ms")

    @commands.command(aliases=['number'])
    async def numbers(
            self, ctx
    ):  #Use {prefix}number,{prefix}numbers, Show random fact about number
        temp = get_number_facts()
        await ctx.send(f"*Did You Know* - {temp}")

    @commands.command(aliases=['fact'])
    async def facts(self,
                    ctx):  #Use {prefix}fact,{prefix}facts, Show random facts
        temp = get_general_facts()
        await ctx.send(f"*Did You Know* - {temp}")

    @commands.command()
    async def math(
            self, ctx, *,
            question):  #Use {prefix}math equation, Solve the given equation
        try:
            await ctx.send(eval(question))
        except:
            await ctx.send("Type a correct equation!!!!")

    @commands.command()
    async def tts(
            self, ctx, *, text
    ):  #Use {prefix}tts text, Convert text to speech and give a mp3 file
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"http://api.voicerss.org/?key={os.getenv('tts_api_token')}&hl=en-us&v=Amy&src={text}"
            ) as response:

                #print("Status:", response.status)
                #print("Content-type:", response.headers['content-type'])

                data = await response.content.read()

                f = discord.File(io.BytesIO(data), filename='test.wav')
                await ctx.send(file=f)
                #await ctx.send(text,tts=True)
                #await ctx.send(response.file)
        '''response = requests.get(f"http://api.voicerss.org/?key={os.getenv('tts_api_token')}&hl=en-us&v=Amy&src={text}")

        print(response.content)
        data = await response.content.read()
        f = discord.File(io.BytesIO(data), filename='test.wav')
        await ctx.send(file=f)'''

    @commands.command()
    async def htts(
            self, ctx, *, text
    ):  #Use {prefix}htts text, Convert text to speech and give a mp3 file in hindi
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"http://api.voicerss.org/?key={os.getenv('tts_api_token')}&hl=hi-in&v=Puja&src={text}"
            ) as response:

                data = await response.content.read()

                f = discord.File(io.BytesIO(data), filename='test.wav')
                await ctx.send(file=f)

    @commands.command()
    async def meme(self, ctx):
        #get_random_memes()

        # assume you have a reddit instance bound to variable `reddit`
        #subreddit = reddit.subreddit("memes")

        #print(subreddit.display_name)  # output: redditdev

        #n = random.randint(1,40)
        #i = 1
        submission = reddit.subreddit("memes").random()
        #print(submission.score)
        #print(submission.comments)
        #print(submission)

        embed = discord.Embed(
            description=
            f'**[{submission.title}](https://www.reddit.com/r/memes/comments/{submission}/)**',
            colour=discord.Colour.blue())

        embed.set_image(url=submission.url)
        embed.set_footer(
            text=f'Requested by {ctx.message.author}',
            icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)
        '''for submission in subreddit.hot(limit=n):
        
        if(i == n):
          print(submission.title)  # Output: the submission's title
          print(submission.score)  # Output: the submission's score
          print(submission.id)     # Output: the submission's ID
          print(submission.url)
          await ctx.send(submission.url)
          break
        else:
          i = i+1'''

    @commands.command()
    async def cmeme(self, ctx):  #coding meme

        #submissions = list(reddit.subreddit('ProgrammerHumor').top(limit=1000))
        #submission = random.choice(submissions)
        submission = reddit.subreddit("ProgrammerHumor").random()

        embed = discord.Embed(
            description=
            f'**[{submission.title}](https://www.reddit.com/r/ProgrammerHumor/comments/{submission}/)**',
            colour=discord.Colour.dark_blue())

        embed.set_image(url=submission.url)
        embed.set_footer(
            text=f'Requested by {ctx.author}',
            icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))

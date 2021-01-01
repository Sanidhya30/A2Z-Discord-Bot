import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    #HELP DESCRIPTION
    @commands.command()
    async def help(self, ctx, *, message=''):
        embed = discord.Embed(
            title='Commands List', colour=discord.Colour.green())

        if (message == ''):
            embed.add_field(
                name=':relieved: FUN', value='`help fun`', inline=True)
            embed.add_field(
                name=':tools: Moderation',
                value='`help moderation`',
                inline=True)
            embed.add_field(
                name=':bikini:NSFW', value='`help nsfw`', inline=True)
            embed.add_field(
                name=':musical_note: Music', value='`help music`', inline=True)
            embed.add_field(
                name=':tada: Giveaway', value='`help giveaway`', inline=True)
        elif (message == 'fun'):
            embed.add_field(
                name=':1234: numbers,number',
                value='`Fetch you some facts about number`',
                inline=True)
            embed.add_field(
                name='😲 facts,fact',
                value='`Fetch you some random facts`',
                inline=True)
            embed.add_field(
                name='📐 math', value='`Solve any equation for you`', inline=True)
            embed.add_field(
                name='🗣 tts', value='`Text-to-speech in english`', inline=True)
            embed.add_field(
                name='🗣 htts', value='`Text-to-speech in hindi`', inline=True)
            embed.add_field(name='😂 meme', value='`Random meme`', inline=True)
            embed.add_field(
                name='👨‍💻 cmeme', value='`Random meme about coding`', inline=True)
        elif (message == 'moderation'):
            embed.add_field(
                name='🗑️ clear',
                value='`Clear the messages for you, specify the amount`',
                inline=True)
            embed.add_field(
                name='⌛ slowmode',
                value='`Enables slowmode in the channel`',
                inline=True)  
            embed.add_field(
                name='🦶 kick',
                value='`Kick member from the server`',
                inline=True)
            embed.add_field(
                name='🚫 ban', value='`Ban member from the server`', inline=True)
            embed.add_field(
                name='🤝 unban',
                value='`Unban member who is banned from the server`',
                inline=True)
        elif (message == 'nsfw'):
            embed.add_field(
                name='🤤 rnsfw', value='`Fetch Random nsfw`', inline=True)
            embed.add_field(
                name='(•)(•) boob,boobs,boobies',
                value='`Random boobies`',
                inline=True)
            embed.add_field(name='😻 pussy', value='`Random pussy`', inline=True)
            embed.add_field(name='🔞 porn', value='`Random porn`', inline=True)
        elif (message == 'music'):
            embed.add_field(
                name='🔗 join', value='`Join the vc you are in`', inline=True)
            embed.add_field(
                name='🦶 leave',
                value='`Clear the song queue and leave the vc`',
                inline=True)
            '''embed.add_field(
                name='volume', value='`Set the volume`', inline=True)'''
            embed.add_field(
                name='⚡ current, playing',
                value='`The current song playing`',
                inline=True)
            embed.add_field(
                name='⏸️ pause',
                value='`Pause the current song playing`',
                inline=True)
            embed.add_field(
                name='⏸️ resume', value='`Resumes the song`', inline=True)
            embed.add_field(name='⏩ skip', value='`Skip the song`', inline=True)
            embed.add_field(
                name='⌛ queue, q', value="`Show the song's queue`", inline=True)
            embed.add_field(
                name='🔀 shuffle', value='`Shuffles the queue`', inline=True)
            embed.add_field(
                name='🤜 remove',
                value='`Remove the song from the queue(Specify index)`',
                inline=True)
            '''embed.add_field(
                name='loop',
                value=
                '`Loop the current song, for unloop use the same command`',
                inline=True)'''
            embed.add_field(
                name='▶️ play, p', value='`Plays a song`', inline=True)
            '''embed.add_field(
                name='volume', value='`Set the volume`', inline=True)'''
        elif (message == 'giveaway'):
            embed.add_field(name = ':tada: gstart', value='`Start a giveaway in the specified channel and ends at the given time`', inline = False)
            embed.add_field(name = '👑 greroll', value='`Reroll the giveaway winners`', inline = False)

        embed.set_footer(
            text='Dont forget to use prefix before using commands')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))

import discord
from discord.ext import commands
from PIL import Image, ImageDraw
import io
import asyncio


def display_board(board):
    blankBoard = """
|-----------------|
|     |     |     |
|  7  |  8  |  9  |
|     |     |     |
|-----------------|
|     |     |     |
|  4  |  5  |  6  |
|     |     |     |
|-----------------|
|     |     |     |
|  1  |  2  |  3  |
|     |     |     |
|-----------------|
"""

    for i in range(1, 10):
        if (board[i] == 'O' or board[i] == 'X'):
            blankBoard = blankBoard.replace(str(i), board[i])
        else:
            blankBoard = blankBoard.replace(str(i), ' ')
    return (blankBoard)


def board_to_image(blankBoard):
    img = Image.new('RGB', (140, 220), color=(41, 40, 38))

    d = ImageDraw.Draw(img)
    d.text((13, 0), blankBoard, fill=(249, 212, 66))

    img.save('game_start.png')


def full_board_check(board):
    return len([x for x in board if x == '#']) == 1


def place_marker(board, marker, position):
    board[position] = marker
    return board


def win_check(board, mark):
    if board[1] == board[2] == board[3] == mark:
        return True
    if board[4] == board[5] == board[6] == mark:
        return True
    if board[7] == board[8] == board[9] == mark:
        return True
    if board[1] == board[4] == board[7] == mark:
        return True
    if board[2] == board[5] == board[8] == mark:
        return True
    if board[3] == board[6] == board[9] == mark:
        return True
    if board[1] == board[5] == board[9] == mark:
        return True
    if board[3] == board[5] == board[7] == mark:
        return True
    return False


class TicTacToe(commands.Cog):
    def __init__(self, client):
        self.client = client

    #TicTacToe COMMANDS
    @commands.command()
    async def xox(self, ctx, amount=1):
        embed = discord.Embed(
            title='Tic Tac Toe', colour=discord.Colour.teal())

        embed.description = 'Waiting for another player, please react to start the game'

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❌")

        await asyncio.sleep(60)  #change it to 60

        #print(self.client.user, ctx.author)
        new_msg = await ctx.channel.fetch_message(msg.id)
        users = await new_msg.reactions[0].users().flatten()
        #print(users, type(users))

        users.pop(users.index(self.client.user))

        if ctx.author in users:
            users.pop(users.index(ctx.author))
        #print(users)

        if not users:
            await ctx.send(
                "Nobody reacted to the message. Terminating the game!!")
            return

        player_1 = ctx.author
        player_2 = users[0]
        embed.description = f"Game is starting in 5 seconds between {player_1.mention}(❌) V/S {player_2.mention}(⭕)"

        await new_msg.clear_reactions()

        await new_msg.edit(embed=embed)

        await asyncio.sleep(5)

        board = ['#'] * 10
        emoji_list = [
            '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'
        ]

        # Set the game up here
        game_on = full_board_check(board)
        player_number = 1
        new_emoji_list = emoji_list.copy() #A temp emoji list so that we can remove the position that have already been used

        while not game_on:
            blankBoard = display_board(board)
            board_to_image(blankBoard)

            if player_number % 2 == 1:
                embed.description = f'{player_1.mention} your turn'
                embed.set_footer(
                        text=f'{player_1} your marker is ❌',
                        icon_url=player_1.avatar_url)
            else:
                embed.description = f'{player_2.mention} your turn'
                embed.set_footer(
                        text=f'{player_2} your marker is ⭕',
                        icon_url=player_1.avatar_url)

            embed.set_image(url="attachment://game_start.png")
            #print(blankBoard)

            f = discord.File('game_start.png')
            msg = await ctx.send(file=f, embed=embed)

            for i in new_emoji_list:
                await msg.add_reaction(i)

            def check_1(reaction, user):
                return user == player_1 and (str(reaction.emoji) in new_emoji_list)

            def check_2(reaction, user):
                return user == player_2 and (str(reaction.emoji) in new_emoji_list)

            try:  #Waiting for the reaction to be added
                if player_number % 2 == 1:
                    reaction, user = await self.client.wait_for(
                        'reaction_add', timeout=30.0, check=check_1)
                else:
                    reaction, user = await self.client.wait_for(
                        'reaction_add', timeout=30.0, check=check_2)
            except asyncio.TimeoutError:
                await ctx.send(
                    "You didn\'t reacted in time, please be quicker next time!"
                )
                return
            else:
                #getting the choice that the player has selected and removing it from the emoji_list
                choice = emoji_list.index(str(reaction.emoji)) + 1
                new_emoji_list.remove(str(reaction.emoji))

                if player_number % 2 == 0:
                    marker = 'O'
                else:
                    marker = 'X'

                board = place_marker(board, marker, int(choice))

                blankBoard = display_board(board)
                board_to_image(blankBoard)

                if win_check(board,
                             marker):  #checks if the user has won or not
                    if player_number % 2 == 1:
                        embed.description = f'🎉Congratulations{player_1.mention} you won the game!!!'
                        embed.set_footer(
                        text=f'{player_1}',
                        icon_url=player_1.avatar_url)
                    else:
                        embed.description = f'🎉Congratulations{player_2.mention} you won the game!!!'
                        embed.set_footer(
                        text=f'{player_2}',
                        icon_url=player_2.avatar_url)

                    embed.set_image(url="attachment://game_start.png")

                    f = discord.File('game_start.png')
                    await ctx.send(file=f , embed=embed)
                    return
                    break

                player_number += 1
                game_on = full_board_check(board)
                #print(emoji_list,new_emoji_list)

        embed.description = 'The game ended in a tie!'
        embed.set_image(url = 'https://thumbs.dreamstime.com/b/better-luck-next-time-rubber-stamp-over-white-background-88415080.jpg')

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(TicTacToe(client))

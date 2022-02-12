# Wordle Discord bot
# aquova, 2022

import discord
import config, db
from wordle import Wordle

client = discord.Client(intents=discord.Intents.default())
games = Wordle()

@client.event
async def on_ready():
    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)
    db.init()

@client.event
async def on_message(message: discord.Message):
    if message.author.id == client.user.id:
        return

    if message.content.startswith("!wordle"):
        try:
            word = message.content.split(" ")[1]
            if word == "restart":
                restarted = games.new_game(message.author.id)
                if restarted:
                    await message.channel.send("Old game abandoned")
                else:
                    await message.channel.send("There was no game in progress")
            elif word == "stats":
                stats = db.get_scores(message.author.id)
                if not stats:
                    await message.channel.send("You have never played!")
                    return
                embed = discord.Embed(title="Your stats", type="rich")
                embed.description = f"You have played {stats[1]} games"
                victories = "```"
                for i in range(6):
                    victories += f"\n{i + 1} | {stats[i + 2]}"
                victories += "```"
                embed.add_field(name="Victories", value=victories)
                await message.channel.send(embed=embed)
            else:
                ret = games.guess(message.author.id, word)
                embed = discord.Embed(title="Wordle!", type="rich")
                embed.description = str(message.author)
                embed.add_field(name=word, value=ret)
                await message.channel.send(embed=embed)
        except IndexError:
            await message.channel.send("Play Wordle in Discord! Send guesses via `!wordle GUESS`")

client.run(config.DISCORD_KEY)

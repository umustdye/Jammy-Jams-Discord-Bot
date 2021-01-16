"""
Author: Heidi Dye
Date: 1/15/2021
Version: 1.0
Purpose: Jammy Jams Music Bot
"""

#Import Discord library
import discord
from discord.ext import commands
#search for videos on YouTube
from youtube_search import YoutubeSearch
#To run python in the console async.
import nest_asyncio

#initialize the client/bot
#client = discord.Client()
client = commands.Bot(command_prefix="!")


"""
#TEST THE YOUTUBE SEARCH--------------
search = "Funny cats"
results = YoutubeSearch(search, max_results=1).to_dict()
#'url_suffix' is the /watch part of the youtube link
print(results)
"""


"""
#sample hello world
@client.event
#async make sures the process happens even if there is a delay in the process
#on_ready is a prebuilt discord function
async def on_ready():
    #connect to the general text channel
    general_channel = client.get_channel(799871091404570657)
    #await waits for the channel to be found before preforming an action
    await general_channel.send("Hello world")
"""

#pop-up message for when the bot enters the voice chat
@client.event
async def on_ready():
        #general text channel
        channel = client.get_channel(799871091404570657)
        await channel.send("Jammy Jams is reporting for duty!")

@client.command()
async def join(ctx):
        #channel = discord.utils.get(ctx.guild.voice_channels, name="General")
        #general voice channel
        channel = client.get_channel(799871091404570658)
        await channel.connect()
        
@client.command()
async def leave(ctx):
        #channel = discord.utils.get(client.voice_clients, guild=ctx.guild)
        channels = client.voice_clients
        for channel in channels:
            if channel.is_connected():
                await channel.disconnect()
            else:
                await ctx.send("The bot is not connected to the voice channel")

#allow nested event loops to run the client/bot in the console
nest_asyncio.apply() 
#run the client/bot(bot token)
client.run("Nzk5ODY4NTI4NDk1ODIwODUw.YAJ1ng.O_pY0IUfXoAXqim3NOZ2F7auutQ")

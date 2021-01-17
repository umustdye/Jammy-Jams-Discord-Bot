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
BOT_TOKEN = ""



#pop-up message for when the bot enters the voice chat
@client.event
async def on_ready():
        #jammy jams messages channel
        jammy_channel = client.get_channel(800145177690898473)
        await jammy_channel.send("Jammy Jams is reporting for duty!")

@client.command()
async def join(ctx):
        #channel = discord.utils.get(ctx.guild.voice_channels, name="General")
        #general voice channel
        channel = client.get_channel(799871091404570658)
        jammy_channel = client.get_channel(800145177690898473)
        await channel.connect()
        await jammy_channel.send("Jammy Jams has entered the party.")
        
        
@client.command()
async def play(ctx, *search_terms):
    #connect to the jammy messages channel
    jammy_channel = client.get_channel(800145177690898473)
    
    
    #put search terms into one string
    search_term = ""
    for term in search_terms:
        search_term += term + " "
    
    #dictionary to hold the search term result from YouTube
    results = YoutubeSearch(search_term, max_results=5).to_dict()
    #if a result was found
    if(results):
        link = 'https://www.youtube.com' + results[0].get('url_suffix')
        await jammy_channel.send(link)
        
    else:
        await jammy_channel.send("Sorry Jammy could not find a cool enough video. Please make your request more specific and try again.")
        

        
@client.command()
async def leave(ctx):
        #channel = discord.utils.get(client.voice_clients, guild=ctx.guild)
        channels = client.voice_clients
        jammy_channel = client.get_channel(800145177690898473)
        for channel in channels:
            if channel.is_connected():
                await channel.disconnect()
                await jammy_channel.send("Jammy Jams has left the music party.")


#allow nested event loops to run the client/bot in the console
nest_asyncio.apply() 
#run the client/bot(bot token)
client.run(BOT_TOKEN)

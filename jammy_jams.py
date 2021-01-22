"""
Author: Heidi Dye
Date: 1/15/2021
Version: 1.0
Purpose: Jammy Jams Music Bot
"""

#Import Discord library
import discord
from discord.ext import commands
from discord.utils import get
from discord import File
#search for videos on YouTube
from youtube_search import YoutubeSearch
#play youtube videos
import youtube_dl
#To run python in the console async.
import nest_asyncio
import asyncio
import os
#To choose random song for shuffle
import random
from collections import deque
import time


#initialize the client/bot
#client = discord.Client()
client = commands.Bot(command_prefix="!")
BOT_TOKEN = ""
song_queue = deque()
master_volume = None

        
    
    
  
async def play_song(ctx, link, video_name):
    yt_opt = {         
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],}
        
    with youtube_dl.YoutubeDL(yt_opt) as yt:
        yt.download([link])
            
            
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    global master_volume
    global song_queue
    guild = ctx.message.guild
    voice_client = ctx.voice_client 
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
            
    #voice_client.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e:print(video_name + " has finished playing"))
    voice_client.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(ctx), client.loop))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
    voice_client.source.volume = float(master_volume)
    
    #voice_client.cleanup()


def connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


async def play_next_song(ctx):
    await asyncio.sleep(2)
    global song_queue
    voice_channel = client.get_channel(799871091404570658)
    text_channel = client.get_channel(800145177690898473)

    time.sleep(.5)
    if(len(song_queue) > 0):
        await text_channel.send(song_queue[0]['video_name'] + " has finished playing.")
        song_queue.popleft()
        song_there = os.path.isfile("song.mp3")
        #await asyncio.sleep(5)
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await text_channel.send("Sorry Jammy cannot play the jams")
            return
        if(len(song_queue)>0):
            await text_channel.send("Preparing song...")
        #
        await play_song(ctx, song_queue[0]['link'], song_queue[0]['video_name'])
        await text_channel.send("Now playing: " + song_queue[0]['video_name'])
        await text_channel.send(song_queue[0]['link'])
        
        
    else:
        await text_channel.send("Jammy Jams is out of song requests.")

#pop-up message for when the bot enters the voice chat
@client.event
async def on_ready():
        #jammy jams messages channel
        jammy_channel = client.get_channel(800145177690898473)
        await jammy_channel.send("Jammy Jams is reporting for duty!")
        global master_volume
        master_volume = 0.40
        

    

@client.command(pass_context = True)
async def join(ctx):
        #channel = discord.utils.get(ctx.guild.voice_channels, name="General")
        #general voice channel
        voice_channel = client.get_channel(799871091404570658)
        text_channel = client.get_channel(800145177690898473)
        await voice_channel.connect()
        await text_channel.send("Jammy Jams has entered the party.")
        
@client.command(pass_context = True)
async def volume(ctx, change):
    guild = ctx.message.guild
    voice_client = ctx.voice_client
    global master_volume
    if(change == "up"):
        #if master_volume <= .9:
        print(master_volume)
        master_volume += 0.1
    if(change == "down"):
        print(master_volume())
        master_volume -= 0.1
        
    else:
        master_volume = 0.4
            
    voice_client.source.volume = float(master_volume)




@client.command(pass_context = True)
async def mute(ctx):
    guild = ctx.message.guild
    voice_client = ctx.voice_client
    global master_volume
    master_volume = 0.0
            
    voice_client.source.volume = float(master_volume)


@client.command(pass_context = True)
async def play(ctx, *, search_term):
    #connect to the jammy messages channel
    text_channel = client.get_channel(800145177690898473)
    #connect to the jammy voice channel
    voice_channel = client.get_channel(799871091404570658)
    global song_queue
    
    #check if the bot is already connected and connect if it is not
    if connected(ctx) == None:
        await voice_channel.connect()
        
    

    #dictionary to hold the search term result from YouTube
    results = YoutubeSearch(search_term, max_results=1).to_dict()
    #if a result was found
    if(results):
        #print(results)
        link = 'https://www.youtube.com' + results[0].get('url_suffix')
        video_name = results[0].get('title')
        next_song = {'video_name':video_name, 'link':link}
        song_queue.append(next_song)

        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await text_channel.send(video_name + " has been added to the queue")

            
            
        else:
        
            song_there = os.path.isfile("song.mp3")
            try:
                if song_there:
                    os.remove("song.mp3")
            except PermissionError:
                    await text_channel.send("Sorry Jammy cannot play the jams")
                    return  
            await text_channel.send("Preparing song...")
            #
            await play_song(ctx, link, video_name)
            await text_channel.send("Now playing: " + video_name)
            await text_channel.send(link)
        
        
    else:
        await text_channel.send("Sorry Jammy could not find a cool enough video. Please make your request more specific and try again.")




@client.command(pass_context = True)
async def queue(ctx, *, search_term):
    #connect to the jammy messages channel
    text_channel = client.get_channel(800145177690898473)
    global song_queue
    #dictionary to hold the search term result from YouTube
    results = YoutubeSearch(search_term, max_results=1).to_dict()
    #if a result was found
    if(results):
        #print(results)
        link = 'https://www.youtube.com' + results[0].get('url_suffix')
        video_name = results[0].get('title')

        #add song to the queue
        await text_channel.send(video_name + " has been added to the queue")
        #await text_channel.send(link)
        next_song = {'video_name':video_name, 'link':link}
        song_queue.append(next_song)
            
        
        
    else:
        await text_channel.send("Sorry Jammy could not find a cool enough video. Please make your request more specific and try again.")



@client.command(pass_context = True)
async def next_song(ctx):
    #connect to the jammy messages channel
    text_channel = client.get_channel(800145177690898473)
    global song_queue
    if(len(song_queue) > 1):
        #add song to the queue
        await text_channel.send(song_queue[1]['video_name'] + " is next in the queue")
        #await text_channel.send(song_queue[0]['link'])
              
    else:
        await text_channel.send("Jammy Jams does not have another song to play")

        
@client.command(pass_context = True)
async def leave(ctx):
    #connect to the jammy messages channel
    text_channel = client.get_channel(800145177690898473)
    #connect to the jammy voice channel
    voice_channel = client.get_channel(799871091404570658)
    channels = client.voice_clients
    for channel in channels:
        if channel.is_connected():
            await channel.disconnect()
            #await jammy_channel.send("Jammy Jams has left the music party.")
            await text_channel.send("Jammy Jams has left the party")
            return
        
    #await voice_channel.disconnect()
    await text_channel.send("Jammy Jams cannot leave a party it was never invited to...")

                

    
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")




@client.command(pass_context = True)
async def pause(ctx):
    #connect to the jammy messages channel
    text_channel = client.get_channel(800145177690898473)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await text_channel.send("Jammy Jams has no audio to pause...")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    #connect to the jammy messages channel
    text_channel = client.get_channel(800145177690898473)
    #connect to the jammy voice channel
    voice_channel = client.get_channel(799871091404570658)
    global song_queue
    
    #check if the bot is already connected and connect if it is not
    if connected(ctx) == None:
        await voice_channel.connect()
        
        
    await text_channel.send("Skipping the current song...")
    ''''  
    #remove the song that was currently playing
    #CHANGE WAS MADE HERE FUTURE HEIDI
    #song_queue.popleft()
    print(song_queue)
    time.sleep(2)
    
    
    if(len(song_queue) > 0):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await text_channel.send("Sorry there are no more songs for Jammy Jams to skip to.")
            return  
        await text_channel.send("Preparing song...")
        #
        await play_song(ctx, song_queue[0]['link'], song_queue[0]['video_name'])
        await text_channel.send("Now playing: " + song_queue[0]['video_name'])
        await text_channel.send(song_queue[0]['link'])
        '''


@client.command(pass_context = True)
async def view_queue(ctx):
    text_channel = client.get_channel(800145177690898473)
    global song_queue
    
    if(len(song_queue) > 0):
        await text_channel.send("Songs in queue...")
        for song in song_queue:
            await text_channel.send(song['video_name'])
            
    else:
        await text_channel.send("Jammy Jams has no current requests")



#allow nested event loops to run the client/bot in the console
nest_asyncio.apply() 
#run the client/bot(bot token)
client.run(BOT_TOKEN)

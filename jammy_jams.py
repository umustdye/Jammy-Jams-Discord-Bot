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
import os
#To choose random song for shuffle
import random


#initialize the client/bot
#client = discord.Client()
client = commands.Bot(command_prefix="!")
BOT_TOKEN = ""
queue = {}
master_volume = None

    

def play_song(ctx, link, video_name):
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
    guild = ctx.message.guild
    voice_client = ctx.voice_client          
    voice_client.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e:print(video_name + " has finished playing"))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
    voice_client.source.volume = float(master_volume)
    
    #voice_client.cleanup()


def connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


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
        print("volume up")
        master_volume += 0.1
    if(change == "down"):
        print("volume down")
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


        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await text_channel.send(video_name + " has been added to the queue")
            next_song = {'video_name':video_name, 'link':link}
            queue.append(next_song)
            
            
        else:
        
            song_there = os.path.isfile("song.mp3")
            try:
                if song_there:
                    os.remove("song.mp3")
            except PermissionError:
                    await text_channel("Sorry Jammy cannot play the jams")
                    return  
            await text_channel.send("Preparing song...")
            play_song(ctx, link, video_name)
            await text_channel.send("Now playing: " + video_name)
            await text_channel.send(link)
        
        
    else:
        await text_channel.send("Sorry Jammy could not find a cool enough video. Please make your request more specific and try again.")

     

        
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










# FOR FUN RANDOM COMMANDS!-----------------------------------------------------------

@client.command(pass_context = True)
async def love(ctx, *, person):
    text_channel = client.get_channel(800145177690898473)
    await text_channel.send("I love you "+ person)
  
@client.command(pass_context = True)
async def love_response(ctx):
    text_channel = client.get_channel(800145177690898473)
    await text_channel.send("I love you more")      
 
@client.command(pass_context = True)    
async def kiss(ctx):
    text_channel = client.get_channel(800145177690898473)
    await text_channel.send("A Heidi kiss for you")
    
    
@client.command(pass_context = True)    
async def fat(ctx):
    text_channel = client.get_channel(800145177690898473)
    await text_channel.send("Wooooooooowwww I am not fat")
    
    
@client.command(pass_context = True)    
async def bigbutt(ctx):
    text_channel = client.get_channel(800145177690898473)
    #connect to the jammy voice channel
    voice_channel = client.get_channel(799871091404570658)
    if (connected(ctx)==None):
        await voice_channel.connect()
    link = 'https://www.youtube.com/watch?v=X53ZSxkQ3Ho'
    video_name = "Baby Got Back"
    file_name = "..\\pictures\\butt.jpg"
    with open(file_name, 'rb') as f:
        await text_channel.send("A Big Butt Heidi for my Honey Bunny")
        await text_channel.send(file=File(f, 'big_butt_heidi.jpg'))
        
        
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await text_channel("Sorry Jammy cannot play the jams")
        return  
    await text_channel.send("Preparing song...")

    play_song(ctx, link, video_name)


@client.command(pass_context = True)    
async def tease(ctx, *, message):
    text_channel = client.get_channel(800145177690898473)
    await text_channel.send("Wooooooooowwww I do not have a "+ message)
    await text_channel.send("Meanie")    
    
    
@client.command(pass_context = True)
async def witch(ctx):
    text_channel = client.get_channel(800145177690898473)
    file_name = "..\pictures\witchy_heidi.png"
    with open(file_name, 'rb') as f:
        await text_channel.send("A Witchy Heidi for my Honey Bunny")
        await text_channel.send(file=File(f, 'witchy_heidi.png'))
        
@client.command(pass_context = True)
async def cuteheidiface(ctx):
    text_channel = client.get_channel(800145177690898473)
    pic_indx = random.randint(1, 11)
    file_name = "..\pictures\cute_heidi\\" + str(pic_indx) + ".jpg"
    with open(file_name, 'rb') as f:
        await text_channel.send("A Cute Faced Heidi for my Honey Bunny")
        await text_channel.send(file=File(f, 'cute_heidi.png'))       


@client.command(pass_context = True)
async def sexyheidi(ctx):
    text_channel = client.get_channel(800145177690898473)
    pic_indx = random.randint(1, 9)
    file_name = "..\pictures\sexy_heidi\\" + str(pic_indx) + ".jpg"
    with open(file_name, 'rb') as f:
        await text_channel.send("A Sexy Heidi for my Honey Bunny")
        await text_channel.send(file=File(f, 'sexy_heidi.png'))   


@client.command(pass_context = True)
async def sebastian(ctx):
    text_channel = client.get_channel(800145177690898473)
    await text_channel.send("Sebastian is Heidi's one and only love in life and she loves him with all her heart")
        
@client.command(pass_context = True)
async def horndog(ctx):
    text_channel = client.get_channel(800145177690898473)
    await text_channel.send("Oh my...")

@client.command(pass_context = True)
async def butt(ctx):
    text_channel = client.get_channel(800145177690898473)
    await text_channel.send("Wowwwwwwwwww")      
        
@client.command(pass_context = True)
async def pew(ctx):
    text_channel = client.get_channel(800145177690898473)
    await text_channel.send("Pew")
    
@client.command(pass_context = True)
async def poke(ctx):
    text_channel = client.get_channel(800145177690898473)
    await text_channel.send("Poke")

#allow nested event loops to run the client/bot in the console
nest_asyncio.apply() 
#run the client/bot(bot token)
client.run(BOT_TOKEN)

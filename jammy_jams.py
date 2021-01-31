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
client = commands.Bot(command_prefix="!")
BOT_TOKEN = ""
song_queue = deque()
song_index = None
master_volume = None
voice_channel_id = 
text_channel_id = 
repeat_song = False
if_play_queue = False
        
    
''' ----- HELPER FUNCTIONS ----- '''   
  
async def play_song(ctx, link, video_name):
    #Jammy Jams text channel to tell the user if Jammy Jams can play the requested song or not
    text_channel = client.get_channel(text_channel_id)
    
    #Jammy Jams volume
    global master_volume

    #The Jammy Jams voice client for playing the song
    voice_client = ctx.voice_client 
    
    #FFMPEG requires a file named song.mp3 to download the song from youtube and play it
    #if the file cannot be overwritten then it throws an exception
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await text_channel.send("Sorry Jammy cannot play the jams")
        return  
    await text_channel.send("Preparing song...")
            

    #Set the settings for the song download
    yt_opt = {         
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],}
        
    #download the song from youtube
    with youtube_dl.YoutubeDL(yt_opt) as yt:
        yt.download([link])
      
    # after the song finishes downloading, tell the user what song is playing
    await text_channel.send("Now playing: " + video_name)
    await text_channel.send(link)        
     
    #rename the downloaded song as song.mp3       
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
            

    
    #use the following commented line if you just want one song to play        
    #voice_client.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e:print(video_name + " has finished playing"))
    
    '''
    Because the voice_client.play() function is not an async function, I cannot call
    another function that is async without the await keyword, so I used the 
    asyncio.run_coroutine_threadsafe() as a replacement for the await keyword
    So after the song finished playing, it'll call the play next function which will prepare
    the next song if there is one
    '''
    voice_client.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(ctx), client.loop))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
    voice_client.source.volume = float(master_volume)
    
    #voice_client.cleanup()


#check if jammy jams is already connected to the voice channel
def connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()



async def play_next_song(ctx):
    await asyncio.sleep(2)
    global song_queue
    global if_play_queue
    #jammy jams voice channel
    voice_channel = client.get_channel(voice_channel_id)
    #jammy jams text channel
    text_channel = client.get_channel(text_channel_id)

    time.sleep(.5)
    
    await text_channel.send(song_queue[0]['video_name'] + " has finished playing.")
    print("Hello")
    print(song_queue)
    print(if_play_queue)
    
    #if the user did not want to repeat the current song then move to the next song in the queue
    if repeat_song == False and if_play_queue == False:
        song_queue.popleft()    
        #if there is another song next in the queue then play that song
        if(len(song_queue)>0):
            await play_song(ctx, song_queue[0]['link'], song_queue[0]['video_name'])
        #if there isn't another song to play next
        else:
            await text_channel.send("Jammy Jams is out of song requests.")
            
    #repeat the current song        
    else:
        if if_play_queue == True:
            if_play_queue = False
            await text_channel.send("Playing from begininng of queue...")
        
            
        if repeat_song == True:
            await text_channel.send("Repeating song...")
        
        await play_song(ctx, song_queue[0]['link'], song_queue[0]['video_name'])
        
    





''' ------- EVENT FUNCTIONS --------- '''
#pop-up message for when the bot enters the voice chat
@client.event
async def on_ready():
        #jammy jams messages channel
        text_channel = client.get_channel(text_channel_id)
        await text_channel.send("Jammy Jams is reporting for duty!")
        global master_volume
        master_volume = 0.40
        




''' ------- COMMAND FUNCTIONS --------'''    

@client.command(pass_context = True)
async def join(ctx):
        voice_channel = client.get_channel(voice_channel_id)
        text_channel = client.get_channel(text_channel_id)
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
    text_channel = client.get_channel(text_channel_id)
    #connect to the jammy voice channel
    voice_channel = client.get_channel(voice_channel_id)
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
        
        #if there is already another song playing, add the requested song to the queue
        #the second part checks if we are not at the end of the song queue
        #if voice.is_playing() or (song_index < len(song_queue)-1):
        if (voice.is_playing() or voice.is_paused()) and len(song_queue) > 0:
            await text_channel.send(video_name + " has been added to the queue")

            
        #if there is curently no song playing play the requested song   
        else:
            await play_song(ctx, link, video_name)

        
        
    else:
        await text_channel.send("Sorry Jammy could not find a cool enough video. Please make your request more specific and try again.")





@client.command(pass_context = True)
async def play_queue(ctx):
    #connect to the jammy messages channel
    text_channel = client.get_channel(text_channel_id)
    #connect to the jammy voice channel
    voice_channel = client.get_channel(voice_channel_id)
    global song_queue
    global if_play_queue
    
    if len(song_queue) > 0:
        #check if the bot is already connected and connect if it is not
        if connected(ctx) == None:
            await voice_channel.connect()
        
    
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        await text_channel.send("Jammy Jams is playing from the begining of the song queue")

        #if there is already a song playing, stop the song and play from the begining of the queue
        if voice.is_playing():
            if_play_queue = True
            voice.stop()

            
        #if there is curently no song playing play from the begining of the song queue   
        else:
            link = song_queue[0]['link']
            video_name = song_queue[0]['video_name']
            await play_song(ctx, link, video_name)

        
        
    else:
        await text_channel.send("Sorry Jammy cannot play from an empty song queue.")




@client.command(pass_context = True)
async def queue(ctx, *, search_term):
    #connect to the jammy messages channel
    text_channel = client.get_channel(text_channel_id)
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
    text_channel = client.get_channel(text_channel_id)
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
    text_channel = client.get_channel(text_channel_id)
    #connect to the jammy voice channel
    voice_channel = client.get_channel(voice_channel_id)
    channels = client.voice_clients
    #turn off repeat 
    global repeat_song
    repeat_song = False
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
    text_channel = client.get_channel(text_channel_id)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await text_channel.send("Jammy Jams has no audio to pause...")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    #turn of repeat
    global repeat_song
    repeat_song = False
    voice.stop()


@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    #connect to the jammy messages channel
    text_channel = client.get_channel(text_channel_id)
    #connect to the jammy voice channel
    voice_channel = client.get_channel(voice_channel_id)
    global song_queue
    
    #check if the bot is already connected and connect if it is not
    if connected(ctx) == None:
        await voice_channel.connect()
        
    #turn of repeat if it was already on
    global repeat_song
    repeat_song = False
    
    await text_channel.send("Skipping the current song...")




@client.command(pass_context = True)
async def view_queue(ctx):
    text_channel = client.get_channel(text_channel_id)
    global song_queue
    
    if(len(song_queue) > 0):
        await text_channel.send("Songs in queue...")
        index = 0
        for song in song_queue:
            await text_channel.send(str(index) + ".) " + song['video_name'])
            index += 1
            
    else:
        await text_channel.send("Jammy Jams has no current requests")
        

@client.command(pass_context = True)
async def clear_queue(ctx):
    text_channel = client.get_channel(text_channel_id)
    global song_queue
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    if voice.is_playing() or voice.pause():
        voice.stop()
        
    if(len(song_queue) > 0):
        await text_channel.send("Jammy Jams is clearing the song queue")
        song_queue.clear()
        
    else:
        await text_channel.send("There are no songs for Jammy Jams to clear")
        
#DO AN ERROR CHECK IF THERE IS A SONG ALREADY PLAYING-----------        
@client.command(pass_context = True)
async def remove(ctx, index):
    global song_queue
    text_channel = client.get_channel(text_channel_id)
    if index>=0 or index < len(song_queue):
        text_channel.send("Removed "+song_queue[index]["video_name"] + " from song queue")
        song_queue.remove(index)
#-------------------------------------------------------------------------------------------

@client.command(pass_context = True)
async def repeat(ctx):
    text_channel = client.get_channel(text_channel_id)
    global repeat_song
    if(repeat_song == False):
        repeat_song = True
        await text_channel.send("Repeat turned on for current song")
        
    else:
       repeat_song = False 
       await text_channel.send("Repeat turned off for current song")




# FOR FUN RANDOM COMMANDS!-----------------------------------------------------------

@client.command(pass_context = True)
async def love(ctx, *, person):
    text_channel = client.get_channel(text_channel_id)
    await text_channel.send("I love you "+ person)
  
@client.command(pass_context = True)
async def love_response(ctx, *, person):
    text_channel = client.get_channel(text_channel_id)
    await text_channel.send("I love you more " + person)      
 
@client.command(pass_context = True)    
async def kiss(ctx):
    text_channel = client.get_channel(text_channel_id)
    await text_channel.send("A Heidi kiss for you")
    
    
@client.command(pass_context = True)    
async def fat(ctx):
    text_channel = client.get_channel(text_channel_id)
    await text_channel.send("Wooooooooowwww I am not fat")
    
    
@client.command(pass_context = True)    
async def bigbutt(ctx):
    text_channel = client.get_channel(text_channel_id)
    #connect to the jammy voice channel
    voice_channel = client.get_channel(voice_channel_id)
    if (connected(ctx)==None):
        await voice_channel.connect()
    link = 'https://www.youtube.com/watch?v=X53ZSxkQ3Ho'
    video_name = "Baby Got Back"
    file_name = "..\\pictures\\butt.jpg"
    with open(file_name, 'rb') as f:
        await text_channel.send("A Big Butt Heidi for my Honey Bunny")
        await text_channel.send(file=File(f, 'big_butt_heidi.jpg'))
        
    global song_queue
    next_song = {'video_name':video_name, 'link':link}
    song_queue.append(next_song)    

    play_song(ctx, link, video_name)


@client.command(pass_context = True)    
async def tease(ctx, *, message):
    text_channel = client.get_channel(text_channel_id)
    await text_channel.send("Wooooooooowwww I do not have a "+ message + "\nMeanie") 
    
    
@client.command(pass_context = True)
async def witch(ctx):
    text_channel = client.get_channel(text_channel_id)
    file_name = "..\pictures\witchy_heidi.jpg"
    with open(file_name, 'rb') as f:
        await text_channel.send("A Witchy Heidi for my Honey Bunny")
        await text_channel.send(file=File(f, 'witchy_heidi.jpg'))
        
@client.command(pass_context = True)
async def cuteheidiface(ctx):
    text_channel = client.get_channel(text_channel_id)
    pic_indx = random.randint(1, 11)
    file_name = "..\pictures\cute_heidi\\" + str(pic_indx) + ".jpg"
    with open(file_name, 'rb') as f:
        await text_channel.send("A Cute Faced Heidi for my Honey Bunny")
        await text_channel.send(file=File(f, 'cute_heidi.png'))   
        
        
@client.command(pass_context = True)
async def boobp(ctx):
    text_channel = client.get_channel(text_channel_id)
    file_name = "..\pictures\\boobp.jpg"
    with open(file_name, 'rb') as f:
        await text_channel.send("Boobp")
        await text_channel.send(file=File(f, 'boobp.jpg'))  


@client.command(pass_context = True)
async def sexyheidi(ctx):
    text_channel = client.get_channel(text_channel_id)
    pic_indx = random.randint(1, 9)
    file_name = "..\pictures\sexy_heidi\\" + str(pic_indx) + ".jpg"
    with open(file_name, 'rb') as f:
        await text_channel.send("A Sexy Heidi for my Honey Bunny")
        await text_channel.send(file=File(f, 'sexy_heidi.png'))   


@client.command(pass_context = True)
async def sebastian(ctx):
    text_channel = client.get_channel(text_channel_id)
    await text_channel.send("Sebastian is Heidi's one and only love in life and she loves him with all her heart")
        
@client.command(pass_context = True)
async def horndog(ctx):
    text_channel = client.get_channel(text_channel_id)
    await text_channel.send("Oh my...")

@client.command(pass_context = True)
async def butt(ctx):
    text_channel = client.get_channel(text_channel_id)
    await text_channel.send("Wowwwwwwwwww")      
        
@client.command(pass_context = True)
async def pew(ctx):
    text_channel = client.get_channel(text_channel_id)
    await text_channel.send("Pew")
    
@client.command(pass_context = True)
async def poke(ctx):
    text_channel = client.get_channel(text_channel_id)
    await text_channel.send("Poke")


@client.command(pass_context = True)
async def boop(ctx):
    text_channel = client.get_channel(text_channel_id)
    await text_channel.send("Boop")
    
@client.command(pass_context = True)
async def meow(ctx):
    text_channel = client.get_channel(text_channel_id)
    await text_channel.send("Meow")

#allow nested event loops to run the client/bot in the console
nest_asyncio.apply() 
#run the client/bot(bot token)
client.run(BOT_TOKEN)

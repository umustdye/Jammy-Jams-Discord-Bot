# Jammy-Jams-Discord-Bot
Jammy Jams is a Discord Bot designed to play and stream music


All commands must be prefixed with !
Jammy Jams must have a predifined text channel to send messages to. Once you have your text channel, get the id and enter this as the value for the "text_channel_id" variable.
Do the same for voice channel.
You also need certain libraries to run Jammy Jams. Please see tthe code to see which ones you need. 

Commands Thus Far....


!play \<song name\>

    Description:
    If there is not a song already playing then Jammy Jams will play the request song from youtube.
    If there a song playing then Jammy Jams will add the requested song to the song queue


!pause

    Description:
    pause the current song


!resume

    Description:
    resume a song that was paused
    
    
!stop !skip

    Description:
    Stops the current song that is playing and skips to the next song in the song queue
    
    
!join

    Description:
    Have Jammy Jams join the Jammy Jams voice channel

!leave

    Description:
    Have Jammy Jams leave the voice channel. The current song that is playing will end though.

!mute


!volume up


!volume down


!queue \<song\>

    Description:
    Add a song to the song queue


!next_song

    Description:
    Shows the next song that is playing in the song queue


!view_queue

    Description:
    Shows the name of all of the songs that arre in the song queue


!repeat

    Description:
    Turn on/off repeat for the current song that is playing
    
!clear_queue

    Description:
    Stops playing the current song and the song queue is cleared

!play_queue

    Description:
    Plays from the beginning of the song queue

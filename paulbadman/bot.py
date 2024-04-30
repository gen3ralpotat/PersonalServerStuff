import discord
from discord.ext import commands
import botconstants
from programmed_responses import check_for_triggers
import asyncio
import json


"""

    Bot Configs

"""

bot_path = botconstants.PATH

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=botconstants.COMMAND_PREFIX,
                   description=botconstants.BOT_DESCRIPTION, intents=intents)

tree = bot.tree

"""

    Bot Events

"""


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.event
async def on_message(message):
    # Dont respond to own message
    if message.author == bot.user:
        return
    # If someone pings
    if bot.user.mentioned_in(message):
        servercount = str(len(bot.guilds))
        await message.channel.send(f"Hey, I am Paul Badman, law representative of this server! You know, folks, I'm not just in one or two servers, oh no! I'm spreading across a {servercount} servers! That's right, {servercount}! I'm like the multi-server maestro, making sure I'm everywhere you need me to be, a {servercount} times over!")
    # check for other triggers
    result = check_for_triggers(message.content)
    if result:
        await message.channel.send(result)
        
    await bot.process_commands(message)
        
"""

    Soundboard

"""

@bot.hybrid_command()
async def sync(ctx: commands.Context):
    await ctx.send("syncing")
    await bot.tree.sync()


@tree.command(name="new", description="Adds an mpeg file as a new sound")
async def new(interaction: discord.Interaction, sound_name: str, sound_file: discord.Attachment):
    # checks for valid file format
    if sound_file.content_type != "audio/mpeg":
        await interaction.response.send_message("Sound is not in mpeg file format")
        return
    
    # loads serversounds.json to variable sounds_json as a dict (find a better way to do this bc json just aint it)
    sounds_json = None
    with open(f"{bot_path}/serversounds.json", "r") as json_file:
        json_file_str = json_file.read()
        sounds_json = json.loads(json_file_str)
        
    # if server has no sounds
    if interaction.guild.id not in sounds_json["servers"]:
        sounds_json["servers"].append(interaction.guild.id)
        sounds_json["sounds"].update({str(interaction.guild.id): []})
    
    # if sound name already in server
    if sound_name in sounds_json["sounds"][str(interaction.guild.id)]:
        await interaction.response.send_message(f"Sound with name `{sound_name}` already exists for server")
        return
    
    # update json variable
    sounds_json["sounds"][str(interaction.guild.id)].append(sound_name)
    
    # save file as .mp3
    with open(f"{bot_path}/sounds/{interaction.guild.id}/{sound_name}.mp3", "wb") as fp:
        await sound_file.save(fp)
        
    # update main json file
    with open(f"{bot_path}/serversounds.json", "w") as json_file:
        json.dump(sounds_json, json_file)
        
    # send confirmation
    await interaction.response.send_message(f"Sound `{sound_name}` successfully added to server")

    
    

@tree.command(name="list", description="Lists all sounds in the server")
async def list(interaction: discord.Interaction):
    # loads serversounds.json to variable sounds_json as a dict (find a better way to do this bc json just aint it)
    sounds_json = None
    with open(f"{bot_path}/serversounds.json", "r") as json_file:
        json_file_str = json_file.read()
        sounds_json = json.loads(json_file_str)
        
    # if server has no sounds
    if interaction.guild.id not in sounds_json["servers"]:
        await interaction.response.send_message(f"Server not registered")
        return 
    
    # send sounds ephemerally (preferably in a better way)
    await interaction.response.send_message(f'{sounds_json["sounds"][str(interaction.guild.id)]}', ephemeral=True)


@tree.command(name="play", description="Plays a sound")
async def play(interaction: discord.Interaction, sound_name: str):
    # if no args provided
    if sound_name is None:
        await interaction.response.send_message("No sound name provided")
        return
    
    # loads serversounds.json to variable sounds_json as a dict
    sounds_json = None
    with open(f"{bot_path}/serversounds.json", "r") as json_file:
        json_file_str = json_file.read()
        sounds_json = json.loads(json_file_str)

    #print(sounds_json)
    
    # if server has no sounds
    if interaction.guild.id not in sounds_json["servers"]:
        await interaction.response.send_message("No sounds for server found")
        return
    
    # if sound not in server
    if sound_name not in sounds_json["sounds"][str(interaction.guild.id)]:
        await interaction.response.send_message(f"No sound with name {sound_name} found for server")
        return
            
            
    # else if sound and server are both good
    
    # voice_state => voice channel the invoker is in
    voice_state=interaction.user.voice
    if voice_state is None:
        await interaction.response.send_message("User not in channel")
    else:
        # i dont like red lines (but they're still everywhere o_o)
        if voice_state.channel is None:
            await interaction.response.send_message("channel is none?")
        else:
            # gets bot's currently connected voice channel
            currently_connected = interaction.guild.voice_client
            # if not connected to same vc as user
            if currently_connected is None:
                channel = await voice_state.channel.connect()
            # if connected to same vc as user
            else:
                # if user channel is not connected channel
                if voice_state.channel != currently_connected.channel: # do not ask me how the fuck this comparison works it just does
                    # dc
                    await currently_connected.disconnect(force=False)
                    currently_connected.cleanup()
                    # re-c
                    channel = await voice_state.channel.connect()
                # if user channel is same as connected channel
                else:
                    # sets channel to current channel
                    channel = currently_connected
            
            # if currently playing
            if channel.is_playing() or channel.is_paused():
                channel.stop()
                
            channel.play(discord.FFmpegPCMAudio(source=f"{bot_path}/sounds/{interaction.guild.id}/{sound_name}.mp3"))
            await interaction.response.send_message(f"Playing sound `{sound_name}`")
            

@tree.command(name="stop", description="Stops currently playing sound")
async def stop(interaction: discord.Interaction):
    currently_connected = interaction.guild.voice_client
    if currently_connected is not None:
        if currently_connected.is_playing() or currently_connected.is_paused():
            currently_connected.stop()
            await interaction.response.send_message("Stopped")
        else:
            await interaction.response.send_message("No sound playing")
    else:
        await interaction.response.send_message("Bot not connected to channel")
            
            
@tree.command(name="pause", description="Pauses currently playing sound")
async def pause(interaction: discord.Interaction):
    currently_connected = interaction.guild.voice_client
    if currently_connected is not None:
        if currently_connected.is_playing():
            currently_connected.pause()
            await interaction.response.send_message("Paused")
        else:
            await interaction.response.send_message("No sound playing")
    else:
        await interaction.response.send_message("Bot not connected to channel")
            
            
@tree.command(name="resume", description="Resumes currently paused sound")
async def resume(interaction: discord.Interaction):
    currently_connected = interaction.guild.voice_client
    if currently_connected is not None:
        if currently_connected.is_paused():
            currently_connected.resume()
            await interaction.response.send_message("Unpaused")
        else:
            await interaction.response.send_message("No sound paused")
    else:
        await interaction.response.send_message("Bot not connected to channel")
            
    
@bot.hybrid_command()
async def shutdown(ctx: commands.Context):
    await ctx.send("closing")
    await bot.close()


"""

    Run the bot

"""


bot.run()
